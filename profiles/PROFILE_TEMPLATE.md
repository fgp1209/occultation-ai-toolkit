# Perfil local del observador

Guarda una copia completada como `profiles/local.md` en el proyecto local o adjúntala al chat. También puede incorporarse a las instrucciones o memoria de un asistente personalizado.

```yaml
site:
  name:
  latitude_deg:
  longitude_deg:
  altitude_m:
  datum:
  coordinate_method:
  coordinate_precision:
  timezone:
  horizon_notes:

equipment:
  telescope:
  aperture_mm:
  focal_length_mm:
  mount:
  camera:
  acquisition_software:
  timing_source:
  timestamp_reference:

validated_limits:
  comfortable_combined_mag:
  prudent_combined_mag:
  minimum_altitude_deg:
  minimum_detectable_drop_mag:
  exposure_ranges:

operations:
  travel_possible:
  sleep_cost:
  setup_minutes:
  notes:
```

No incluyas contraseñas, tokens, direcciones privadas ni otros secretos.
