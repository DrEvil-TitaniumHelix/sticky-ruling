# Opens a test ruling, checks it shows, keeps focus, stacks, and returns the answer. Run: python selftest.py
import ctypes,subprocess,time,os,sys
u=ctypes.windll.user32;b=ctypes.create_unicode_buffer(200);R=os.path.join(os.path.dirname(os.path.abspath(__file__)),'ruling.py')
def fg():u.GetWindowTextW(u.GetForegroundWindow(),b,200);return b.value
f0=fg();E={**os.environ,'RULING_SELFTEST':'1','HOME':os.environ.get('TEMP','.'),'USERPROFILE':os.environ.get('TEMP','.')}
p=[subprocess.Popen([sys.executable,R,f'SELFTEST {i}','Closes by itself.','A: first','B: second'],env=E,stdout=subprocess.PIPE,text=True)for i in(1,2)]
time.sleep(1);f1=fg();vis=all(u.FindWindowW(None,f'Sticky ruling: SELFTEST {i}')for i in(1,2));out=[x.communicate(timeout=20)[0].strip()for x in p]
assert vis,'window not shown';assert f0==f1,f'focus stolen: {f0!r}->{f1!r}';assert out==[f'RULING SELFTEST {i}: A: first'for i in(1,2)],out
print('PASS: 2 windows shown, focus kept, answers returned')
