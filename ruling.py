# sticky-ruling: always-on-top window holding a ruling's full context while the session keeps working.
# Windows: tested. macOS/Linux: needs python3-tk, untested.
# Run via Bash run_in_background. Exits printing "RULING <item>: <answer>" when clicked; stop the task to close it after an inline reply.
# usage: python ruling.py "Item 12 of 35" "question + context" "A: option + trade-off" "B: ..." [...]
import sys,json,time,os,ctypes,tkinter as tk
from pathlib import Path
item,q,opts=sys.argv[1],sys.argv[2],sys.argv[3:]
LOG=Path.home()/'.claude/rulings/rulings.log';LOG.parent.mkdir(parents=True,exist_ok=True)
WIN=os.name=='nt';T='Sticky ruling: ';n=[0]
if WIN:
  from ctypes import wintypes as w;u=ctypes.windll.user32;prev=u.GetForegroundWindow();b=ctypes.create_unicode_buffer(64)
  try:ctypes.windll.shcore.SetProcessDpiAwareness(1)
  except Exception:pass
  u.EnumWindows(ctypes.WINFUNCTYPE(w.BOOL,w.HWND,w.LPARAM)(lambda h,_:(u.GetWindowTextW(h,b,64),n.__setitem__(0,n[0]+b.value.startswith(T)))and 1),0)  # stack below open rulings
r=tk.Tk();r.title(T+item);r.attributes('-topmost',1);r.configure(bg='#1e1e2e');r.geometry(f'+{80+n[0]*40}+{80+n[0]*40}')
F=('Segoe UI',13);W=900;L=dict(bg='#1e1e2e',justify='left',wraplength=W)
def done(a):
  LOG.open('a',encoding='utf-8').write(json.dumps({'t':time.strftime('%F %T'),'item':item,'q':q,'answer':a})+'\n');print(f'RULING {item}: {a}',flush=True);r.destroy()
WR=[]  # widgets whose wrap width follows the window width, so a narrower window re-wraps instead of clipping words
x=tk.Label(r,text=item,font=('Segoe UI',16,'bold'),fg='#f9e2af',**L);x.pack(anchor='w',padx=16,pady=(14,4));WR.append((x,0))
x=tk.Label(r,text=q,font=F,fg='#cdd6f4',**L);x.pack(anchor='w',padx=16,pady=4);WR.append((x,0))
for o in opts:
  x=tk.Button(r,text=o,font=F,wraplength=W,justify='left',anchor='w',bg='#313244',fg='#cdd6f4',activebackground='#45475a',relief='flat',padx=10,pady=8,command=lambda o=o:done(o));x.pack(fill='x',padx=16,pady=4);WR.append((x,24))
def rewrap(ev):
  if ev.widget is r:
    wl=max(240,ev.width-32)
    for x,pad in WR:x.configure(wraplength=wl-pad)
r.bind('<Configure>',rewrap)
e=tk.Entry(r,font=F,bg='#313244',fg='#cdd6f4',insertbackground='#cdd6f4')
def other():
  if WIN:h=int(r.wm_frame(),16);u.SetWindowLongW(h,-20,u.GetWindowLongW(h,-20)&~0x08000000)  # allow keyboard focus for typing
  e.pack(fill='x',padx=16,pady=4);e.focus_force();e.bind('<Return>',lambda _:e.get().strip() and done('OTHER: '+e.get().strip()))
tk.Button(r,text='Other (type an answer, Enter to send)',font=F,bg='#1e1e2e',fg='#a6adc8',relief='flat',command=other).pack(anchor='w',padx=16)
x=tk.Label(r,text='Or just answer in the terminal, naming this item.',font=('Segoe UI',11),fg='#7f849c',**L);x.pack(anchor='w',padx=16,pady=(4,14));WR.append((x,0))
r.protocol('WM_DELETE_WINDOW',r.iconify)  # X minimizes: a ruling never vanishes unanswered
if WIN:  # WS_EX_NOACTIVATE: never steals focus. ponytail: mac/linux may briefly take focus on open; add per-WM no-focus hints if it bites
  r.update_idletasks();h=int(r.wm_frame(),16);u.SetWindowLongW(h,-20,u.GetWindowLongW(h,-20)|0x08000000)
  r.after(50,lambda:u.GetForegroundWindow()!=prev and u.SetForegroundWindow(prev))
if os.environ.get('RULING_SELFTEST'):r.after(2000,lambda:done(opts[0]))
r.mainloop()
