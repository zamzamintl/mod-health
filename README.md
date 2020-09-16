Sistema Municipal de Atención Social de la Dirección General de Desarrollo Social de la Alcaldía Bolivariana de Maracaibo. Estado Zulia, Venezuela.

SisteMASo
=========

# Pre-requisitos:
- Devuan 2.
- Python 3.
- Odoo 13.
- Mejoras visuales:
    git clone https://github.com/OCA/web --depth 1
    git clone https://github.com/odoo-mastercore/odoo_ux
- Localización para Venezuela:
    git clone https://github.com/odoo-mastercore/odoo-venezuela
- Códigos de área:
    git clone https://github.com/rhe-mastercore/vzla_code/
- source odoo-13/venv/bin/activate venv
- Para generar los brazaletes con QR:
        sudo apt-get install libfreetype6-dev
- sudo pip3.8 install phonenumbers pyqrcodeng pypng
<!-- - Para traer los datos del CNE:
        sudo apt-get install python3-beautifulsoup python3-bs4 m2crypto
- Para generar los documentos en PDF:
        sudo aptitude purge wkhtmltopdf
        wget -c https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.4/wkhtmltox-0.12.4_linux-generic-amd64.tar.xz
        tar -ixvf wkhtmltox-0.12.4_linux-generic-amd64.tar.xz
        sudo cp wkhtmltox/bin/wkhtmltopdf /usr/local/bin/wkhtmltopdf
        sudo cp wkhtmltox/bin/wkhtmltoimage /usr/local/bin/wkhtmltoimage
        rm wkhtmltox* -r -->

# Instalación:
- En .odoorc_sistemaso:
    addons_path = /home/angel/code/odoo-13.0/odoo/addons,/home/angel/code/odoo-13.0/addons,/home/angel/code/SisteMASo,/home/angel/code/web,,/home/angel/code/odoo_ux,/home/angel/code/odoo-venezuela,/home/angel/code/vzla_code
- Entrar en modo debug (?debug=1#).
- Actualizar lista de módulos.
- Instalar módulo website.
- Instalar módulo web_responsive.
- Instalar módulo backend_theme.
- Instalar módulo l10n_ve_base.
- Instalar todos los demás módulos:

-i aguila_base,base_locale_uom_default,case_general,cdi_data,comm_media,\
event_history,fleet_vehicle_type,health_lifestyle,housing,medical,\
medical_center,medical_disease,medical_insurance,medical_medicament,\
medical_medicament_attributes,medical_medication,medical_pathology,\
medical_pathology_icd10,medical_pathology_import,medical_pharmacy,\
medical_pharmacy_us,medical_practitioner,medical_prescription,\
medical_prescription_state,medical_prescription_thread,medical_procedure,\
parish_structure,pasi_data,sistemaso_base,social,territorial_pd,\
territorial_pd_ext_mbo,vzla_legal

# Post-instalación:
- Settings -> General Settings:
    - Business Documents -> Format:
        - Cambiar formato de papel a carta.
    - Contacts:
        - Desactivar partner Autocomplete.
    - Users:
        - Activar Password Reset (restauración de contraseña).
        - Luego de migrar la data: Desactivar Importar/Exportar
    - Integrations:
        - Desactivar Unsplash Image Library. Guardar.
- Settings -> Website:
    - Website Title
        - Cambiar nombre y Favicon.
    - Website Logo:
        - Establecer logo de la Alcaldía.
    - Customer Account:
        - Por invitación.
    - Features:
        - Desactivar múltiples websites. Guardar.
    - Languages:
        - Instalar Español VE.
        - Seleccionar Español VE.
        - Establecer Español VE como predeterminado.
        - Eliminar Inglés. Guardar.
- Administrador -> Preferences:
    - Language: Seleccionar Español VE.
    - Timezone: America/Caracas. Guardar.
- Settings -> General Settings -> Languages -> Manage Languages:
    - Activar: Spanish VE.
    - Establecer Lunes como primer día de la semana. Guardar.
    - Archivar inglés.
- Ajustes -> Traducciones -> Términos Traducidos:
    - Cambiar Valor de Traducción: «¡No se encontrarón archivos!» por «No hay registros. Cree uno.».

Credits
=======

This system is based on GNU Health (gnuhealth.org), and on modules in
* http://hg.savannah.gnu.org/hgweb/health/
* https://github.com/OCA/partner-contact

This version
------------
* Ángel Ramírez Isea <angel.ramirez.isea@yandex.com>

GNU Health creator
------------------
* Dr. Luis Falcón, MD <falcon@gnuhealth.org>

``medical`` Original Contributors
---------------------
* Dave Lasley <dave@laslabs.com>
* Jonathan Nemry <jonathan.nemry@acsone.eu>
* Brett Wood <bwood@laslabs.com>
* Jordi Ballester Alomar <jordi.ballester@eficent.com>

The current project as it is today represents an evolution of the original work
started by Luis Falcon. See https://sourceforge.net/projects/medical/files/Oldfiles/1.0.1,
that later became GNU Health (see
http://health.gnu.org/). The original code was licensed under GPL.

On Nov 27, 2012 derivative code was published in https://github.com/OCA/vertical-medical,
by Tech-Receptives Solutions Pvt. Ltd., licensed
under AGPL.  The license change was unauthorized by the original
author. See https://github.com/OCA/vertical-medical/commit/f0a664749edaea36f6749c34bfb04f1fc4cc9ea4

On Feb 17, 2017 the branch 9.0 of the project was relicensed to LGPL.
https://github.com/OCA/vertical-medical/pull/166. Various prior contributors
approved the relicense, but not all.

On Jan 25, 2018, GNU Health claimed that the original code and attribution
should be respected, and after further investigation the Odoo Community
Association Board agreed to switch the license back to GPL v3 to respect the
rights of the original author.

Although no trace of relationship was found between the code at the date
and the original code from 2012, through the commit history of the project one
can see that the current status of the project is the end result of an
evolutionary process. The Odoo Community Association Board concluded that
the original license should be respected for ethical reasons.

More information can be read here - https://odoo-community.org/blog/our-blog-1/post/vertical-medical-75.

Maintainer
----------

This module is maintained by Asociaciones Cooperativas  de
Procesamiento Unificado Informático, R.S.; Simón Rodríguez para el
Conocimiento Libre, R.S.; y Soluciones Informáticas para el
Desarrollo de Inclusión Social, R.S.

To contribute to this module, please visit https://git.labviv.org.ve.
