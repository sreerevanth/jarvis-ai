import sys
sys.path.insert(0, 'D:/J.A.R.V.I.S')

try:
    from voice import speak, listen
    print('voice ok')
    from brain import ask_gemini
    print('brain ok')
    from skills.system_control import get_time
    print('system ok')
    from skills.web_tasks import search_google
    print('web ok')
    from skills.notes import take_note
    print('notes ok')
    print('ALL GOOD')
except Exception as e:
    import traceback
    traceback.print_exc() 
