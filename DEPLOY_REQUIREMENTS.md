# DEPLOY REQUIREMENTS

🚀 Deploy requirements for IH-IT software

## App Template

    - Api (api.wsgi)
  

## System

    - Linux

## Environment

    - Dev
    - Prod

## App folder

    `apimsp`

## Distribution

    - Master

## Url GIT

    - ssh://git@github.com:IHCantabria/msp.tools.git

## DNS

_Production_

    - apimsp.ihcantabria.com

_Development_

    - apimspdev.ihcantabria.com

## Other settings

Select only if needed:

**Python version**

`3.6`

** Others **

**Services to restart**

`apache2`

**Backup**

    - Tags
    - Snapshot
    - Clone/Backup

---

**Do you need any other configuration?**

* Ejecutar requirements.txt
* Modificar `{{ app }}/env_{{ app }}/lib/python3.6/site-packages/msptools/config.py`:
    - valor para `filepath`: `"/dat/{{ app }}/log/api.log"`

* Permisos `0755` para directorios:
    - path: "{{ item.ruta }}"
    - owner: "{{ item.user }}"
    - group: "{{ item.grupo }}"
    - mode: "{{ item.permiso }}"
    

## Relationships

**What applications, services, or data sources is this application related to?**

`_______________________________________________________________________________`

## Credits

[IH Cantabria](https://github.com/IHCantabria)

## FAQ

- Document provided by the system administrators [David del Prado](https://ihcantabria.com/directorio-personal/tecnologo/david-del-prado-secadas/) y [Gloria Zamora](https://ihcantabria.com/directorio-personal/tecnologo/gloria-zamora/)
