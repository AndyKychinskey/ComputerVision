from dataclasses.dataclasses import *

"""
load data
"""
# json parser
parsed_json = JSON_Object('test_data.json')
parsed_json = parsed_json.get_object()
# points for validation
pointer_on_main_template = Validation_Point('validation_points', 'pointer_on_main_template', parsed_json)
stop_after_Continue_template = Validation_Point('validation_points', 'stop_after_Continue_template', parsed_json)
stop_after_Step_over_template = Validation_Point('validation_points', 'stop_after_Step_over_template', parsed_json)
# load templates of buttons
reset_device_btn_template = GUI_Object('debug_btns', 'reset_device_btn_template', parsed_json,
										pointer_on_main_template,
										'stopped on main()',
										wait_in_cycle=True)

continue_btn_template = GUI_Object('debug_btns', 'continue_btn_template', parsed_json,
									stop_after_Continue_template,
									'after pointer_on_main_template')
step_over_btn_template = GUI_Object('debug_btns', 'step_over_btn_template', parsed_json,
									stop_after_Step_over_template,
									'stop_after_Step_over_template')

restart_btn_template = GUI_Object('debug_btns', 'restart_btn_template', parsed_json,
									pointer_on_main_template,
									'stopped on main()',
									wait_in_cycle=True)

stop_btn_template = GUI_Object('debug_btns', 'stop_btn_template', parsed_json)
# work with watch window
watch_window_template = GUI_Object('watch_window', 'watch_window_template', parsed_json)
add_var_to_watch_window_btn_template = GUI_Object('watch_window', 'add_var_to_watch_window_btn_template', parsed_json)
watch_window_counter_var_template = GUI_Object('watch_window', 'watch_window_counter_var_template', parsed_json)
# launch configurations (LCs) section: name of LC, buttons, etc
run_and_debug_active = GUI_Object('launch_configs', 'run_and_debug_active', parsed_json)
run_and_debug_unactive = GUI_Object('launch_configs', 'run_and_debug_unactive', parsed_json)
launch_configs_list = GUI_Object('launch_configs', 'launch_configs_list', parsed_json)
launch_KitProg_LC = GUI_Object('launch_configs', 'launch_KitProg_LC', parsed_json)
start_debugging_btn_unactive = GUI_Object('launch_configs', 'start_debugging_btn_unactive', parsed_json)
start_debugging_btn_active = GUI_Object('launch_configs', 'start_debugging_btn_active', parsed_json)
watch_window = GUI_Object('launch_configs', 'watch_window', parsed_json)

# test scenario
scenario = (continue_btn_template,
			step_over_btn_template,
			continue_btn_template,
			reset_device_btn_template,
			continue_btn_template,
			restart_btn_template,
			continue_btn_template,
			stop_btn_template)
# object handler
handler = GUI_Object_Handler()
"""
start of scenario
"""
# start launch configuration
if handler.check_result_with_template(run_and_debug_active):
	handler.locate_template_on_screen(run_and_debug_active, need_to_click=True)
	print("run_and_debug_active")
elif handler.check_result_with_template(run_and_debug_unactive):
	handler.locate_template_on_screen(run_and_debug_unactive, need_to_click=True)
	print("run_and_debug_unactive")

# click on list of launch configurations list
pyagui.sleep(0.5)
handler.locate_template_on_screen(launch_configs_list, need_to_click=True)
pyagui.move(0, 200, 0.5)
# click on KitProg Launch Configuration
pyagui.sleep(0.5)
handler.locate_template_on_screen(launch_KitProg_LC, need_to_click=True)
# run KitProg Launch Configuration
pyagui.sleep(0.5)
handler.locate_template_on_screen(start_debugging_btn_unactive, need_to_click=True)
# wait till pointer will be on main()
while not handler.check_result_with_template(pointer_on_main_template):
	pyagui.sleep(5)
else:
	print("Stopped on main() : successfully found in cycle")
# click on watch window
pyagui.sleep(0.5)
handler.locate_template_on_screen(watch_window, need_to_move_to=True)
pyagui.click()
# adding value to track to window
pyagui.sleep(0.5)
handler.locate_template_on_screen(watch_window_template, need_to_click=True)
pyagui.sleep(0.5)
handler.locate_template_on_screen(add_var_to_watch_window_btn_template, need_to_click=True)
# input with pyautogui
pyagui.write('counter', interval=0.25)
pyagui.press('enter')


for idx, step in enumerate(scenario):
    print(f'step idx is {idx}')
    handler.locate_template_on_screen(step, threshold=0.9, need_to_click=True)
    pyagui.sleep(1)

    if step.is_validation_point:
    	if not step.is_wait_in_cycle:
    		if not handler.check_result_with_template(step.get_validation_object()):
    			raise Exception(f"{step.comment_to_validation_point()} : not valid")
    		else:
    			print(f"{step.comment_to_validation_point()} : valid")
    	elif step.is_wait_in_cycle:
    		while not handler.check_result_with_template(step.get_validation_object()):
    			pyagui.sleep(5)
    		else:
    			print(f"{step.comment_to_validation_point()} : valid")

    pyagui.sleep(4)
