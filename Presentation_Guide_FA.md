# راهنمای اجرای پروژه و ارائه در کلاس

این پروژه برای درس **Methods of Optimization and Decision Making** است.
هدف، پیدا کردن جای کمینه‌ی یک تابع یک‌متغیره بدون محاسبه‌ی مشتق و مقایسه‌ی
تعداد محاسبات تابع در پنج روش است.

## اول برنامه را روی کامپیوتر خودت اجرا کن

۱. فایل ZIP را Extract کن. پوشه‌ای را باز کن که `main.py` داخل آن است.
در همان پوشه CMD را باز کن؛ دستورهای زیر را یکی‌یکی اجرا کن:

```bat
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python main.py
python research.py
python -m unittest -v
```

اگر محیط مجازی را قبلاً ساخته‌ای، دوباره ساختنش لازم نیست؛ فقط فعالش کن.
اگر نصب کتابخانه‌ی رسم نمودار ممکن نبود، عددها همچنان با دستور زیر محاسبه می‌شوند:

```bat
python main.py --no-plots
```

نمودارهای مثال اصلی از قبل در پوشه‌ی `results` هستند. تست‌ها باید با `OK`
تمام شوند و اجرای مثال اصلی باید `Reference check: PASS` نشان بدهد.

اگر نوت‌بوک را ترجیح می‌دهی، `Optimization_Demo.ipynb` را در VS Code باز کن،
کرنل پایتون محیط خودت را انتخاب کن و سلول‌ها را از بالا اجرا کن. این نوت‌بوک
همان فایل‌های الگوریتم را فراخوانی می‌کند؛ نسخه‌ی دیگری از روش‌ها نیست.

## مثال ما چیست

تابع را این‌طور تعریف کرده‌ایم:

\[
f(x)=1+(x-\sqrt{2})^2+0.2(x-\sqrt{2})^4,\qquad -2\le x\le5.
\]

کمینه‌ی دقیق در `x = sqrt(2)` یعنی تقریباً **۱٫۴۱۴۲** است و مقدار کمینه **۱** است.
علت ساده است: جمله‌های توان دوم و چهارم منفی نمی‌شوند و فقط در همان نقطه صفرند.
هرچه فاصله از این نقطه بیشتر شود، مقدار تابع بیشتر می‌شود. بنابراین تا رسیدن
به آن نزولی و بعد از آن صعودی است. برای این توضیح هیچ مشتقی نگرفته‌ایم.

نمودار `results/objective.png` همین رفتار را نشان می‌دهد. نمودار به‌تنهایی
برای اثبات یونیمودال بودن هر تابع دلخواه کافی نیست؛ در مثال ما استدلال بالا هم وجود دارد.

الگوریتم‌ها مقدار جواب دقیق را دریافت نمی‌کنند. فقط تابع، دو سر بازه و دقت
به آن‌ها داده می‌شود. جواب دقیق بعداً برای بررسی نتیجه به کار می‌رود.

## دقت یعنی چه

`delta = 0.001` یعنی فاصله‌ی جواب تقریبی از **محل کمینه** باید حداکثر ۰٫۰۰۱ باشد.
این عدد، خطای مقدار تابع نیست.

هر روش یک بازه‌ی کوچک نگه می‌دارد که کمینه داخل آن است. وقتی طول آن حداکثر
`2 * delta` شد، وسط بازه را جواب می‌گیریم. دورترین نقطه‌ی این بازه از وسطش
فقط نصف طول بازه فاصله دارد؛ برای همین خطا حداکثر `delta` است.

اگر استاد دقت را «طول بازه‌ی نهایی» تعریف کرده باشد، باید مقدار موردنظرش را
بر دو تقسیم کنی و به‌عنوان `delta` به برنامه بدهی. تعریف ما در گزارش روشن نوشته شده است.

## هر روش چه می‌کند

| روش | توضیح ساده برای خودت |
|---|---|
| Uniform search | کل بازه را با فاصله‌های کوچک نمونه‌برداری می‌کند و اطراف بهترین نقطه را نگه می‌دارد. |
| Sequential scan | از چپ جلو می‌رود؛ وقتی مقدار تابع دیگر کمتر نشد، اطراف نقطه‌ی قبلی را نگه می‌دارد. |
| Dichotomy | نزدیک وسط، دو نقطه می‌گذارد و با مقایسه‌ی مقدار تابع، بخشی از بازه را حذف می‌کند. |
| Golden section | دو نقطه با نسبت طلایی می‌گذارد و در ادامه یکی از محاسبات قبلی را دوباره استفاده می‌کند. |
| Fibonacci | از نسبت عددهای فیبوناچی استفاده می‌کند؛ تعداد مراحل از ابتدا با توجه به دقت تعیین می‌شود. |

تعریف جستجوی ترتیبی را حتماً با اسلاید استاد مقایسه کن. نسخه‌ی این پروژه
«پیمایش شبکه تا اولین افزایش» است. اگر استاد روش قدم افزایشی یا روش دیگری گفته باشد،
این بخش باید مطابق همان اسلاید تغییر کند.

## شمارنده چرا مهم است

در یک مسئله‌ی واقعی ممکن است محاسبه‌ی تابع یک شبیه‌سازی گران باشد. بنابراین
کمتر صدا زدن تابع، هزینه را کمتر می‌کند. در این پروژه زمان اجرا معیار اصلی نیست.

`N search` تعداد محاسبات حین جستجو است. `N total` یک محاسبه‌ی دیگر برای
نمایش مقدار تابع در جواب نهایی هم دارد. تعداد محاسبات مربوط به رسم نمودار و
اعتبارسنجی وارد این شمارنده‌ها نمی‌شود.

برای `delta = 0.001` خروجی واقعی این است:

| روش | تعداد کل محاسبات تابع |
|---|---:|
| Uniform search | 7002 |
| Sequential scan | 3417 |
| Dichotomy | 25 |
| Golden section | 19 |
| Fibonacci | 19 |

همه‌ی روش‌ها دقت خواسته‌شده را رعایت کرده‌اند. لازم نیست روشی که کمترین
محاسبه را دارد در هر آزمایش اتفاقاً نزدیک‌ترین عدد به جواب دقیق را هم بدهد.
مقایسه‌ی منصفانه، هزینه‌ی رسیدن به **یک دقت تضمین‌شده‌ی مشترک** است.

## تغییر تابع جلوی استاد

فایل `problem.py` را باز کن. این موارد را عوض کن:

```python
def objective_function(x):
    return (x - 0.37)**2 + 2.0

A = -1.0
B = 2.0
DELTAS = (0.1, 0.01, 0.001)
DESCRIPTION = "f(x) = (x - 0.37)^2 + 2"
REFERENCE_X = None
REFERENCE_F = None
```

این فقط یک مثال برای تمرین تغییر تابع است. تابع و بازه‌ای را که استاد می‌دهد
جای آن قرار بده. در پایتون توان با `**` نوشته می‌شود، نه `^`.
برای لگاریتم از `math.log(x)`، نمایی از `math.exp(x)` و ریشه از `math.sqrt(x)` استفاده کن.
باید تابع روی تمام بازه تعریف شده باشد و یونیمودال بودن آن را بررسی کنی.

اگر جواب دقیق تابع جدید را نمی‌دانی، دو مقدار `REFERENCE` را `None` بگذار
تا برنامه جواب قبلی را معیار قرار ندهد. فایل را ذخیره کن و اجرا کن:

```bat
python main.py --output results_live
```

این دستور خروجی تازه را در پوشه‌ی جدا می‌نویسد. گزارش Word و PDF خودکار عوض
نمی‌شود؛ گزارش آماده مربوط به مثال اصلی است. اگر در نوت‌بوک کار می‌کنی، بعد از
ذخیره‌ی `problem.py` سلول‌ها را از اول اجرا کن تا تغییرات دوباره بارگذاری شوند.

## متن کوتاه انگلیسی برای ارائه

متن زیر را با فهمیدن معنی آن تمرین کن:

> My project compares five methods for one-dimensional minimization without derivatives.
> I chose a unimodal function on the interval from minus two to five.
> The graph shows that the function decreases before the minimum and increases after it.
> I implemented uniform search, sequential scan, dichotomy, golden section, and Fibonacci search.
> All methods use the same accuracy definition, and I count every objective function evaluation.
> Golden section and Fibonacci reuse previous function values, so they need fewer evaluations.
> I checked the answers using the known minimum and the final intervals.
> To solve a new problem, I only change the function, the interval, and the accuracy in problem.py.

معنی: پروژه‌ام پنج روش کمینه‌سازی یک‌بعدی بدون مشتق را مقایسه می‌کند. تابعی
یونیمودال روی بازه‌ی منفی دو تا پنج انتخاب کردم. نمودار نشان می‌دهد که تابع
قبل از کمینه نزولی و بعد از آن صعودی است. هر پنج روش را پیاده‌سازی کردم،
برای همه تعریف دقت یکسان دارم و محاسبات تابع را می‌شمارم. گلدن سکشن و
فیبوناچی با استفاده‌ی دوباره از مقدارهای قبلی، محاسبات کمتری لازم دارند.
جواب‌ها را با کمینه‌ی معلوم و بازه‌ی نهایی بررسی کردم. برای مسئله‌ی جدید
فقط تعریف تابع، بازه و دقت را در فایل مسئله عوض می‌کنم.

## سؤال‌های احتمالی استاد

**Why did you choose Python?**

> Python makes the algorithms easy to read and test. It also provides convenient tools for plots and numerical experiments. The objective function is separated from the search methods.

**Why is your function unimodal without using derivatives?**

> Its value increases with the distance from the square root of two. Therefore, it decreases before this point and increases after it.

**Why do you stop at an interval width of two delta?**

> I return the midpoint. Its maximum possible error is half the interval width.

**Is Fibonacci always better than golden section?**

> Fibonacci can give a smaller final interval for a fixed evaluation budget. Golden section is simpler and can continue without choosing the final number of steps in advance. In my experiments, they sometimes use the same number of evaluations.

**One long Fibonacci run or several short runs?**

> In my restart experiment, one long run needs no more evaluations and needs fewer evaluations at the finer accuracies. Restarting discards stored values and starts a new search plan on the remaining interval.

**How did you validate the program?**

> I checked the exact solution, the width and containment of every final interval, and the function counters. I also tested different functions, boundary minima, and invalid inputs.

**Why do several methods print the same value of the function?**

> The function is very flat near the minimum, and the displayed values are rounded. The final intervals and the error in x show the differences more clearly.

## ترتیب پیشنهادی نمایش در کلاس

۱. گزارش و تعریف مسئله را باز کن.

۲. نمودار تابع را نشان بده و یونیمودال بودن را توضیح بده.

۳. `problem.py` و سپس شمارنده و دو الگوریتم در `algorithms.py` را نشان بده.

۴. `python main.py` را اجرا کن و جدول تعداد محاسبات را توضیح بده.

۵. برای بخش تحقیق، `python research.py` و قسمت مربوط به فیبوناچی گزارش را نشان بده.

۶. تابع جدید استاد را وارد کن، ذخیره کن و خروجی تازه بگیر.

قبل از تحویل، نام و شماره‌ی گروه خودت را به صفحه‌ی اول Word اضافه کن و در
صورت نیاز از Word دوباره PDF بگیر. نام دانشجو و استاد عمداً حدس زده نشده است.

پیام کامیت پیشنهادی برای آرشیو پروژه:

```text
Add derivative-free one-dimensional optimization project and report
```
