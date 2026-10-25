# Conventions

- Python: four spaces, type hints for public functions, descriptive names.
- Keep HTTP handlers thin; isolate provider and scoring logic in services.
- Validate user inputs; treat provider data as untrusted.
- Escape provider strings before rendering in browser UI.
- Avoid unnecessary logs of precise user locations.
- Use environment variables; never commit secrets.
- Add tests for edge cases and provider failures.
- Keep docs, schemas, frontend, and API response models synchronized.
