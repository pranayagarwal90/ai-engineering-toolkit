# Maintenance command evidence

Confirm local environment commands from the project. Inspect composer.json and composer.lock before selecting package targets. composer show, composer why and composer prohibits can help explain dependency constraints; verify syntax using installed command help.

A Composer dry run may use network/cache even when manifest changes are disabled. Choose exact packages and targets; inspect scripts/plugins before any real solver operation. Do not update every dependency by default. Confirm backups, update-hook/config procedures and existing audit/quality commands in the target project. Verify locked, installed and deployed evidence separately.
