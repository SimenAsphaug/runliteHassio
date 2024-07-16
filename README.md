# RuneLite Integration

This is a custom integration for Home Assistant that integrates with RuneLite to provide farming patch timers.

## Installation

1. Install HACS if you haven't already.
2. Add this repository to HACS as a custom repository.
3. Install the "RuneLite Integration" via HACS.
4. Add the following configuration to your `configuration.yaml` file:

```yaml
sensor:
  - platform: runelite
