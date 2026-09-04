# Manifiesto de evento

```yaml
event:
  body:
  star:
  event_date_utc:
  prediction_source:
  prediction_version:

station:
  name:
  coordinates_source:
  coordinates_status:

capture:
  original_file:
  original_hash:
  camera_settings_file:
  timing_log_file:
  start_utc:
  end_utc:
  exposure_s:
  camera:
  timing_source:
  timestamp_reference:
  dropped_frames_status:

field:
  target_confirmed_by:
  wcs_or_chart:
  comparison_stars:

reduction:
  software_versions:
  lightcurve_file:
  analysis_report:
  d_utc:
  d_uncertainty_s:
  r_utc:
  r_uncertainty_s:
  duration_s:

classification:
  result:
  detectability_evidence:
  limitations:

report:
  draft_file:
  attachments:
  review_status:
```

Los campos desconocidos quedan vacíos o marcados `AUSENTE`; nunca se completan desde otro evento.
