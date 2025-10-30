if getattr(config, "motherShip_boss_active", False):
            boss_present = any(e.character_type == "enemy8" for e in enemy_group) # keep track if there is a carrier mothership in the group(exist)
            if boss_present:
                config.motherShip_boss_active = True
            # Only clear the flag if it was active and there are NO boss enemies left
            elif not boss_present and config.mothership_wave < wave_count : # if now carrier boss and we are in diffrent wave than boss spawn wave
                config.motherShip_boss_active = False