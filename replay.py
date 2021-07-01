import obspython as obs
import winsound
import time
hotkey_id = obs.OBS_INVALID_HOTKEY_ID
autorestart = True

print("script loaded")


def on_event(pressed):
	if not pressed:
		#WHY DOES THIS WORK>?????
		time.sleep(1)
		obs.obs_frontend_replay_buffer_stop()
		return
	obs.obs_frontend_replay_buffer_save()

def restartReplay():
	if (obs.obs_frontend_replay_buffer_active() == False and autorestart):
		obs.obs_frontend_replay_buffer_start()
	obs.remove_current_callback()
	obs.timer_add(restartReplay, 2000)


def script_update(settings):
	global autorestart
	autorestart = obs.obs_data_get_bool(settings,"autoRestart")
	return


def script_description():
	return "Save and wipe replay buffer"


def checkBox(props, prop, *args, **kwargs):  # pass settings implicitly
	return

def script_properties():
	props = obs.obs_properties_create()
	ar = obs.obs_properties_add_bool(props, "autoRestart", "Auto restart buffer.")
	obs.obs_property_set_modified_callback(ar, checkBox)
	return props



def script_load(settings):
	obs.timer_add(restartReplay, 2000)
	global hotkey_id
	hotkey_id = obs.obs_hotkey_register_frontend("on_event.trigger", "Save and Wipe Replay", on_event)
	hotkey_save_array = obs.obs_data_get_array(settings, "on_event.trigger")
	obs.obs_hotkey_load(hotkey_id, hotkey_save_array)
	obs.obs_data_array_release(hotkey_save_array)




def script_save(settings):
	hotkey_save_array = obs.obs_hotkey_save(hotkey_id)
	obs.obs_data_set_array(settings, "on_event.trigger", hotkey_save_array)
	obs.obs_data_array_release(hotkey_save_array)