# Perfil local del observador

Guarda una copia completada como `profiles/local.md` en un proyecto editable. Para GPT/Gem/Project, descarga la copia como `observer-profile.md` y súbela a sus archivos. En un chat con memoria, guarda datos estables solo tras autorización explícita.

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
  timing_characterization_status:

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

profile_metadata:
  created_at:
  last_confirmed_at:
  source: user_confirmed
  persistence:
```

No incluyas contraseñas, tokens, direcciones privadas ni otros secretos.

Las coordenadas aproximadas bastan para radar. Las coordenadas exactas del trípode para reporte deben mantenerse separadas cuando revelen una ubicación privada.
