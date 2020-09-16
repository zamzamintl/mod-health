# Copyright (C) 2008-2020 Luis Falcon <lfalcon@gnusolidario.org>
# Copyright (C) 2011-2020 GNU Solidario <health@gnusolidario.org>
# Copyright 2020 LabViv.
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from odoo import api, fields, models
from datetime import datetime


class InpatientRegistration(models.Model):
    """Patient admission History"""
    _name = 'inpatient.registration'
    _description = "Patient admission History"
    icu = fields.Boolean(
        'ICU',
        help='The patient was admitted to ICU during hospitalization'
    )
    icu_admissions = fields.One2many(
        'inpatient.icu',
        'name',
        "ICU Admissions"
    )


class InpatientIcu(models.Model):
    _name = 'inpatient.icu'
    _description = "Patient ICU Information"

    def icu_duration(self, name):
        if self.discharged_from_icu:
            end = self.icu_discharge_date
        else:
            end = datetime.now()
        return end.date() - self.icu_admission_date.date()

    name = fields.Many2one(
        'inpatient.registration',
        'Registration Code',
    )
    admitted = fields.Boolean(
        'Admitted',
        help="The patient is currently admitted at ICU",
        default=True
    )
    icu_admission_date = fields.Datetime(
        'ICU Admission',
        help="ICU Admission Date",
    )
    discharged_from_icu = fields.Boolean('Discharged')
    icu_discharge_date = fields.Datetime(
        'Discharge on',
        states={
            'discharged_from_icu': [('invisible', False), ('required', True)]
        }
    )
    # TODO: a computed field
    # icu_stay = fields.Function(fields.TimeDelta('Duration'), 'icu_duration')
    icu_stay = fields.Datetime('icu_duration')
    mv_history = fields.One2many(
        'icu.ventilation',
        'name',
        "Mechanical Ventilation History"
    )

    @api.depends('discharged_from_icu')
    def on_change_with_admitted(self):
        # Reset the admission flag when the patient is discharged from ICU
        if self.discharged_from_icu:
            res = False
            self.icu_discharge_date = datetime.today()
        else:
            res = True
            self.icu_discharge_date = False
        return res


class Glasgow(models.Model):
    """Glasgow Coma Scale"""
    _name = 'icu.glasgow'
    _description = 'Glasgow Coma Scale'

    name = fields.Many2one(
        'inpatient.registration',
        'Registration Code',
        required=True
    )
    evaluation_date = fields.Datetime(
        'Date',
        default=datetime.now(),
        required=True
    )
    glasgow = fields.Integer(
        'Glasgow',
        default=15,
        help='Level of Consciousness on Glasgow Coma Scale: <9 severe, 9-12 '
        'Moderate, >13 minor'
    )
    glasgow_eyes = fields.Selection(
        [
            ('1', '1: Does not Open Eyes'),
            ('2', '2: Opens eyes in response to painful stimuli'),
            ('3', '3: Opens eyes in response to voice'),
            ('4', '4: Opens eyes spontaneously'),
        ],
        'Eyes',
        default='4'
    )
    glasgow_verbal = fields.Selection(
        [
            ('1', '1: Makes no sounds'),
            ('2', '2: Incomprehensible sounds'),
            ('3', '3: Utters inappropriate words'),
            ('4', '4: Confused, disoriented'),
            ('5', '5: Oriented, converses normally'),
        ],
        'Verbal',
        default='5'
    )
    glasgow_motor = fields.Selection(
        [
            ('1', '1: Makes no movement'),
            ('2', '2: Extension to painful stimuli - decerebrate response'),
            ('3', '3: Abnormal flexion to painful stimuli - decort. response'),
            ('4', '4: Flexion/Withdrawal to painful stimuli'),
            ('5', '5: Localizes painful stimuli'),
            ('6', '6: Obeys commands'),
        ],
        'Motor',
        default='6'
    )

    @api.onchange('glasgow_verbal', 'glasgow_motor', 'glasgow_eyes')
    def on_change_with_glasgow(self):
        self.glasgow = int(self.glasgow_motor) + int(self.glasgow_eyes) + \
            int(self.glasgow_verbal)

    # Return the Glasgow Score with each component
    def name_get(self):
        if self.name:
            res = str(self.glasgow) + ': E' + self.glasgow_eyes + ' V' + \
                self.glasgow_verbal + ' M' + self.glasgow_motor
            return res


class ApacheII(models.Model):
    """Apache II scoring"""
    _name = 'icu.apache2'
    _description = 'Apache II scoring'

    name = fields.Many2one(
        'inpatient.registration',
        'Registration Code',
        required=True
    )
    score_date = fields.Datetime('Date', required=True)
    age = fields.Integer('Age', help='Patient age in years')
    temperature = fields.Float('Temperature', help='Rectal temperature')
    mean_ap = fields.Integer('MAP', help='Mean Arterial Pressure')
    heart_rate = fields.Integer('Heart Rate')
    respiratory_rate = fields.Integer('Respiratory Rate')
    fio2 = fields.Float('FiO2')
    pao2 = fields.Integer('PaO2')
    paco2 = fields.Integer('PaCO2')
    aado2 = fields.Integer('A-a DO2')
    ph = fields.Float('pH')
    serum_sodium = fields.Integer('Sodium')
    serum_potassium = fields.Float('Potassium')
    serum_creatinine = fields.Float('Creatinine')
    arf = fields.Boolean('ARF', help='Acute Renal Failure')
    wbc = fields.Float(
        'WBC',
        help="White blood cells x 1000/ml. 4500 wbc/ml = 4.5"
    )
    hematocrit = fields.Float('Hematocrit')
    gcs = fields.Integer(
        'GSC',
        help='Last Glasgow Coma Scale. You can use the GSC calculator from '
        'the Patient evaluation Form.'
    )
    chronic_condition = fields.Boolean(
        'Chronic condition',
        help='Organ Failure or immunocompromised patient'
    )
    hospital_admission_type = fields.Selection(
        [
            ('blank', '-'),
            ('me', 'Medical or emergency postoperative'),
            ('el', 'elective postoperative')
        ], 'Hospital Admission Type'
    )
    # TODO: is domain in views states={
    #    'invisible': Not(Bool(('chronic_condition'))),
    #    'required': Bool(('chronic_condition'))}, sort=False)
    apache_score = fields.Integer('Score')

    # Default FiO2 PaO2 and PaCO2 for A-a gradient calculat. w/non-null values
    @api.onchange('fio2', 'pao2', 'paco2')
    def on_change_with_aado2(self):
        # Calculates the Alveolar-arterial difference
        # based on FiO2, PaCO2 and PaO2 values
        if self.fio2 and self.paco2 and self.pao2:
            self.aado2 = (713.0 * self.fio2) - (self.paco2 / 0.8) - self.pao2

    @api.onchange(
        'age', 'temperature', 'mean_ap', 'heart_rate', 'respiratory_rate',
        'fio2', 'pao2', 'aado2', 'ph', 'serum_sodium', 'serum_potassium',
        'serum_creatinine', 'arf', 'wbc', 'hematocrit', 'gcs',
        'chronic_condition', 'hospital_admission_type'
    )
    def on_change_with_apache_score(self):
        # Calculate the APACHE SCORE from the variables
        total = 0
        if self.age:
            if 44 < self.age < 55:
                total = total + 2
            elif 54 < self.age < 65:
                total = total + 3
            elif 64 < self.age < 75:
                total = total + 5
            elif self.age > 74:
                total = total + 6
        if self.temperature:
            if (38.5 <= self.temperature < 39) or \
               (34 <= self.temperature < 36):
                total = total + 1
            elif 32 <= self.temperature < 34:
                total = total + 2
            elif (30 <= self.temperature < 32) or \
                 (39 <= self.temperature < 41):
                total = total + 3
            elif self.temperature >= 41 or self.temperature < 30:
                total = total + 4
        if self.mean_ap:
            if (110 <= self.mean_ap < 130) or (50 <= self.mean_ap < 70):
                total = total + 2
            elif 130 <= self.mean_ap < 160:
                total = total + 3
            elif 160 <= self.mean_ap or self.mean_ap < 50:
                total = total + 4
        if self.heart_rate:
            if (55 <= self.heart_rate < 70) or (110 <= self.heart_rate < 140):
                total = total + 2
            elif (40 <= self.heart_rate < 55) or \
                 (140 <= self.heart_rate < 180):
                total = total + 3
            elif 180 <= self.heart_rate or self.heart_rate < 40:
                total = total + 4
        if self.respiratory_rate:
            if (10 <= self.respiratory_rate < 12) or \
               (25 <= self.respiratory_rate < 35):
                total = total + 1
            elif 6 <= self.respiratory_rate < 10:
                total = total + 2
            elif 35 <= self.respiratory_rate < 50:
                total = total + 3
            elif 50 <= self.respiratory_rate or self.respiratory_rate < 6:
                total = total + 4
        if self.fio2:
            # If Fi02 is greater than 0.5, we measure the AaDO2 gradient
            # Otherwise, we take into account the Pa02 value
            if self.fio2 >= 0.5:
                if 200 <= self.aado2 < 350:
                    total = total + 2
                elif 350 <= self.aado2 < 500:
                    total = total + 3
                elif self.aado2 >= 500:
                    total = total + 4
            else:
                if 61 <= self.pao2 < 71:
                    total = total + 1
                elif 55 <= self.pao2 < 61:
                    total = total + 3
                elif self.pao2 < 55:
                    total = total + 4
        if self.ph:
            if 7.5 <= self.ph < 7.6:
                total = total + 1
            elif 7.25 <= self.ph < 7.33:
                total = total + 2
            elif (7.15 <= self.ph < 7.25) or (7.6 <= self.ph < 7.7):
                total = total + 3
            elif self.ph >= 7.7 or 7.15 > self.ph:
                total = total + 4
        if self.serum_sodium:
            if 150 <= self.serum_sodium < 155:
                total = total + 1
            elif (155 <= self.serum_sodium < 160) or \
                 (120 <= self.serum_sodium < 130):
                total = total + 2
            elif (160 <= self.serum_sodium < 180) or \
                 (111 <= self.serum_sodium < 120):
                total = total + 3
            elif 180 <= self.serum_sodium or self.serum_sodium < 111:
                total = total + 4
        if self.serum_potassium:
            if (3 <= self.serum_potassium < 3.5) or \
               (5.5 <= self.serum_potassium < 6):
                total = total + 1
            elif 2.5 <= self.serum_potassium < 3:
                total = total + 2
            elif 6 <= self.serum_potassium < 7:
                total = total + 3
            elif 7 <= self.serum_potassium or self.serum_potassium < 2.5:
                total = total + 4
        if self.serum_creatinine:
            arf_factor = 1
            if self.arf:
                # We multiply by 2 the score if there is concomitant ARF
                arf_factor = 2
            if (self.serum_creatinine < 0.6) or \
               (1.5 <= self.serum_creatinine < 2):
                total = total + 2 * arf_factor
            elif 2 <= self.serum_creatinine < 3.5:
                total = total + 3 * arf_factor
            elif self.serum_creatinine >= 3.5:
                total = total + 4 * arf_factor
        if self.hematocrit:
            if 46 <= self.hematocrit < 50:
                total = total + 1
            elif (50 <= self.hematocrit < 60) or (20 <= self.hematocrit < 30):
                total = total + 2
            elif self.hematocrit >= 60 or self.hematocrit < 20:
                total = total + 4
        # WBC ( x 1000 )
        if self.wbc:
            if 15 <= self.wbc < 20:
                total = total + 1
            elif (20 <= self.wbc < 40) or (1 <= self.wbc < 3):
                total = total + 2
            elif self.wbc >= 40 or self.wbc < 1:
                total = total + 4
        # Immnunocompromised or severe organ failure
        if self.chronic_condition:
            if self.hospital_admission_type == 'me':
                total = total + 5
            else:
                total = total + 2
        self.apache_score = total


class MechanicalVentilation(models.Model):
    """Mechanical Ventilation History"""
    _name = 'icu.ventilation'
    _description = 'Mechanical Ventilation History'

    def mv_duration(self, name):
        start = end = datetime.now()
        if self.mv_start:
            start = self.mv_start
        if self.mv_end:
            end = self.mv_end
        return end.date() - start.date()

    name = fields.Many2one(
        'inpatient.icu',
        'Patient ICU Admission',
        required=True
    )
    ventilation = fields.Selection(
        [
            ('none', 'None - Maintains Own'),
            ('nppv', 'Non-Invasive Positive Pressure'),
            ('ett', 'ETT'),
            ('tracheostomy', 'Tracheostomy')
        ],
        'Type',
        help="NPPV: Non-Invasive Positive Pressure, BiPAP-CPAP, ETT: "
        "Endotracheal Tube"
    )
    ett_size = fields.Integer(
        'ETT Size',
        states={'ventilation': [('invisible', 'ett')]}
    )
    # TODO change to false
    tracheostomy_size = fields.Integer('Tracheostomy size')
    # TODO states={'invisible': Not(Equal(('ventilation'), 'tracheostomy'))})
    mv_start = fields.Datetime(
        'From', help="Start of Mechanical Ventilation", required=True
    )
    mv_end = fields.Datetime('To', help="End of Mechanical Ventilation",)
    # TODO states={ 'invisible': Bool(('current_mv')),
    #    'required': Not(Bool(('current_mv')))}
    # TODO a compute field
    # mv_period = fields.Function(fields.TimeDelta('Duration'), 'mv_duration')
    mv_period = fields.Datetime('mv_duration')
    current_mv = fields.Boolean('Current', default=True)
    remarks = fields.Char('Remarks')


class ChestDrainageAssessment(models.Model):
    """Chest Drainage Asessment"""
    _name = 'icu.chest.drainage'
    _description = 'Chest Drainage Asessment'

    name = fields.Many2one('patient.rounding', 'Rounding', required=True)
    location = fields.Selection(
        [
            ('blank', '-'),
            ('rl', 'Right Pleura'),
            ('ll', 'Left Pleura'),
            ('mediastinum', 'Mediastinum')
        ],
        'Location',
        sort=False
    )
    fluid_aspect = fields.Selection(
        [
            ('blank', '-'),
            ('serous', 'Serous'),
            ('bloody', 'Bloody'),
            ('chylous', 'Chylous'),
            ('purulent', 'Purulent')
        ],
        'Aspect',
        sort=False
    )
    suction = fields.Boolean('Suction')
    suction_pressure = fields.Integer(
        'cm H2O',
        states={'suction': [('invisible', False), ('required', True)]}
    )
    oscillation = fields.Boolean('Oscillation')
    air_leak = fields.Boolean('Air Leak')
    fluid_volume = fields.Integer('Volume')
    remarks = fields.Char('Remarks')


class PatientRounding(models.Model):
    # Nursing Rounding for ICU
    # Inherit and append to the existing model the new functionality for ICU
    _name = 'patient.rounding'
    _description = 'Chest Drainage Asessment'

    STATES = {'done': [('readonly', True)]}
    icu_patient = fields.Boolean(
        'ICU',
        help='Check if Intensive Care Unit rounding.',
        states=STATES
    )
    gcs = fields.Many2one(
        'icu.glasgow',
        'GCS',
        domain=[('name', '=', ('name'))],
        states=STATES
    )
    pupil_dilation = fields.Selection(
        [
            ('normal', 'Normal'),
            ('miosis', 'Miosis'),
            ('mydriasis', 'Mydriasis')
        ],
        'Pupil Dilation',
        default='normal',
        sort=False,
        states=STATES
    )
    left_pupil = fields.Integer('L', help="Size in mm", states=STATES)
    right_pupil = fields.Integer('R', help="Size in mm", states=STATES)
    anisocoria = fields.Boolean('Anisocoria', states=STATES)
    pupillary_reactivity = fields.Selection(
        [
            ('blank', '-'),
            ('brisk', 'Brisk'),
            ('sluggish', 'Sluggish'),
            ('nonreactive', 'Nonreactive')
        ],
        'Pupillary Reactivity',
        sort=False,
        states=STATES
    )
    pupil_consensual_resp = fields.Boolean(
        'Consensual Response',
        help="Pupillary Consensual Response",
        states=STATES
    )
    respiration_type = fields.Selection(
        [
            ('blank', '-'),
            ('regular', 'Regular'),
            ('deep', 'Deep'),
            ('shallow', 'Shallow'),
            ('labored', 'Labored'),
            ('intercostal', 'Intercostal')
        ],
        'Respiration',
        sort=False,
        states=STATES
    )
    oxygen_mask = fields.Boolean('Oxygen Mask', states=STATES)
    fio2 = fields.Integer('FiO2', states=STATES)
    peep = fields.Boolean('PEEP', states=STATES)
    peep_pressure = fields.Integer('cm H2O', help="Pressure")
    # TODO: states={'invisible': Not(Bool(('peep'))),
    # 'required': Bool(('peep')), 'readonly': ('state') == 'done'}
    sce = fields.Boolean('SCE', help="Subcutaneous Emphysema", states=STATES)
    lips_lesion = fields.Boolean('Lips lesion', states=STATES)
    oral_mucosa_lesion = fields.Boolean('Oral mucosa lesion', states=STATES)
    chest_expansion = fields.Selection(
        [
            ('blank', '-'),
            ('symmetric', 'Symmetrical'),
            ('asymmetric', 'Asymmetrical')
        ],
        'Expansion',
        sort=False,
        states=STATES
    )
    paradoxical_expansion = fields.Boolean(
        'Paradoxical',
        help="Paradoxical Chest Expansion",
        states=STATES
    )
    tracheal_tug = fields.Boolean('Tracheal Tug', states=STATES)
    trachea_alignment = fields.Selection(
        [
            ('blank', '-'),
            ('midline', 'Midline'),
            ('right', 'Deviated right'),
            ('left', 'Deviated left')
        ],
        'Tracheal alignment',
        sort=False,
        states=STATES
    )
    chest_drainages = fields.One2many(
        'icu.chest.drainage',
        'name',
        "Drainages",
        states=STATES
    )
    xray = fields.Binary('Xray', states=STATES)
    # TODO: ecg = fields.Many2one('gnuhealth.patient.ecg', 'Inpatient ECG',
    #  domain=[('inpatient_registration_code', '=', ('name'))],states=STATES)
    venous_access = fields.Selection(
        [
            ('blank', '-'),
            ('none', 'None'),
            ('central', 'Central catheter'),
            ('peripheral', 'Peripheral')
        ],
        'Venous Access',
        sort=False,
        states=STATES
    )
    swan_ganz = fields.Boolean(
        'Swan Ganz',
        help="Pulmonary Artery Catheterization (PAC)",
        states=STATES
    )
    arterial_access = fields.Boolean('Arterial Access', states=STATES)
    dialysis = fields.Boolean('Dialysis', states=STATES)
    edema = fields.Selection(
        [
            ('blank', '-'),
            ('none', 'None'),
            ('peripheral', 'Peripheral'),
            ('anasarca', 'Anasarca')
        ],
        'Edema',
        sort=False,
        states=STATES
    )
    bacteremia = fields.Boolean('Bacteremia', states=STATES)
    ssi = fields.Boolean('Surgery Site Infection', states=STATES)
    wound_dehiscence = fields.Boolean('Wound Dehiscence', states=STATES)
    cellulitis = fields.Boolean('Cellulitis', states=STATES)
    necrotizing_fasciitis = fields.Boolean(
        'Necrotizing fasciitis',
        states=STATES
    )
    vomiting = fields.Selection(
        [
            ('blank', '-'),
            ('none', 'None'),
            ('vomiting', 'Vomiting'),
            ('hematemesis', 'Hematemesis')
        ],
        'Vomiting',
        sort=False,
        states=STATES
    )
    bowel_sounds = fields.Selection(
        [
            ('blank', '-'),
            ('normal', 'Normal'),
            ('increased', 'Increased'),
            ('decreased', 'Decreased'),
            ('absent', 'Absent')
        ],
        'Bowel Sounds',
        sort=False,
        states=STATES
    )
    stools = fields.Selection(
        [
            ('blank', '-'),
            ('normal', 'Normal'),
            ('constipation', 'Constipation'),
            ('diarrhea', 'Diarrhea'),
            ('melena', 'Melena')
        ],
        'Stools',
        sort=False,
        states=STATES
    )
    peritonitis = fields.Boolean('Peritonitis signs', states=STATES)

    @api.onchange('left_pupil', 'right_pupil')
    def on_change_with_anisocoria(self):
        if (self.left_pupil == self.right_pupil):
            self.anisocoria = False
        else:
            self.anisocoria = True
