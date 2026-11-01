# KLAVA — Windows Portable და ინსტალატორი

ვერსია: 1.2 · 2026-10-28 · კანონიკური ტექნიკური HANDOUT.

## მიზანი და საზღვრები

Windows 10/11 x64-ისთვის გასავრცელებელი ZIP შეიცავს მხოლოდ:

```text
KLAVA/KLAVA.exe
KLAVA/exercises.txt
```

მომხმარებელს Python-ის ან ინსტალატორის დაყენება არ სჭირდება. ZIP ჯერ სრულად ამოიღეთ;
ორივე ფაილი ერთად გადაიტანეთ. `exercises.txt` შეინახეთ UTF-8 ფორმატით (BOM დასაშვებია).
გამოიყენეთ მინიმუმ ორი არაცარიელი ხაზი; თითო ხაზზე ერთი დავალება.
არსებული წესით კიდეების გამოტოვებები იჭრება, ცარიელი ხაზები გამოტოვდება და ასოები დიდდება.
აქტიური კლავიატურა მხარს უჭერს A–Z ასოებსა და SPACE-ს. სხვა სიმბოლოს (მძიმე, ციფრი,
TAB, ქართული ასო) შემცველი ფაილით სესია არ დაიწყება: პროგრამა kiosk რეჟიმამდე აჩვენებს
შეცდომას ხაზის ნომრითა და სიმბოლოთი (`logic/exercise_text.py`). პაკეტიზაცია ამ წესებს არ ცვლის.
ფაილის ცვლილება აისახება შემდეგი სესიის დაწყებისას. პროგრამა სავარჯიშოებს არ გადაწერს.

## გარემო და საწყისი მტკიცებულება

საწყისი `main`: `95aa336da47fe4f7cf7de07c96661fb459901539`.
PR #5 ცალკე რჩება; მისი behavioral guard შესწორება ამ სამუშაოში არ შედის.
`data/sentences.txt` შეიცავს ექვს არაცარიელ თავსებად ხაზს და უცვლელად კოპირდება.
პროგრამა იყენებს Python standard library-სა და Tkinter-ს; მესამე მხარის runtime
Python პაკეტები არ სჭირდება. კონსტიტუცია უკვე `main`-ზეა, თუმცა მის სათაურში
ისტორიული Proposed ტექსტი რჩება; ეს სამუშაო მმართველობით ტექსტს არ ცვლის.

## მიზეზი და არქიტექტურა

თავდაპირველად `Trainer` რესურსებისა და დავალების ფარდობით ბილიკებს მიმდინარე
სამუშაო კატალოგიდან კითხულობდა. shortcut-ით ან სხვა კატალოგიდან გაშვება არასანდო იყო.

- `logic/resources.py::bundled_path`: მოდულის `__file__`-იდან პოულობს პროექტის ან
  PyInstaller-ის დროებითი გაშლის root-ს. იღებს ბილიკს, აბრუნებს `Path`-ს; არაფერს წერს.
- `logic/resources.py::exercise_path`: frozen რეჟიმში იყენებს `sys.executable`-ის
  მშობელ კატალოგს და `exercises.txt`-ს. source რეჟიმში ინარჩუნებს config-ის ბილიკს,
  პროექტის root-ის მიმართ. არ მართავს სესიას.
- `logic/config.py::Config`: კითხულობს ჩაშენებულ config-ს.
- `Trainer._load_sentences`: UTF-8/UTF-8 BOM წაკითხვა და არსებული ნორმალიზაცია;
  არასწორ კოდირებაზე გასაგები ლოკალიზებული შეცდომა. `start_training` ჯერ ამოწმებს
  ფაილსა და ორ ხაზს, მხოლოდ შემდეგ ააქტიურებს kiosk-ს.
- `KLAVA.spec`: onefile/windowed, `config.ini`, მთელი `resources/` და LICENSE შიგნით;
  Tkinter/Tcl/Tk და Python ბიბლიოთეკებს PyInstaller აგროვებს. `data/` არ იფუთება,
  რადგან გარე ფაილის არყოფნა არ უნდა დაიმალოს ჩაშენებულზე გადართვით.

`Trainer` რჩება კონტროლერად; UI, განლაგება, ფერები და სასწავლო ზღვრები უცვლელია.
`--onefile` გაშვებისას რესურსები დროებით იშლება სისტემურ temp-ში. ეს აუცილებელი
runtime ქცევაა და EXE-ის გვერდით მუდმივ დამატებით ფაილებს არ ქმნის.

საფუძველი: [PyInstaller runtime paths](https://pyinstaller.org/en/stable/runtime-information.html)
და [spec ფაილები](https://pyinstaller.org/en/stable/spec-files.html).

## განმეორებადი აწყობა Windows-ზე

რეპოზიტორიის root-იდან, Python 3.11 x64 გარემოში:

```powershell
python -m pip install pyinstaller==6.16.0 pytest==8.4.2 ruff==0.14.2
python -m pytest -q
python -m ruff check .
python -m PyInstaller --clean --noconfirm KLAVA.spec
python scripts/package_windows.py
```

შედეგი: `dist/KLAVA-windows-x64.zip`. `.spec` არჩეულია, რათა რესურსების სია და
windowed/onefile პარამეტრები ვერსიონირებადი იყოს. ავტომატიზაცია:
[Windows Portable workflow](../.github/workflows/windows-portable.yml).
ტრიგერები: PR და `workflow_dispatch`; `contents: read`; secrets არ გამოიყენება.
ხელით UI-დან გაშვება workflow-ის default branch-ზე მოხვედრის შემდეგაა ხელმისაწვდომი.
ამ სამუშაო შტოს პირველი build PR-ის გახსნით იწყება; merge საჭირო არ არის.
არ არის schedule, Release, deployment ან ახალი Slack შეტყობინების მექანიზმი.

ყოველი run ცალკე checkout-ში იგება. პაკეტიზაცია აკოპირებს მხოლოდ ორ დასახელებულ
ფაილს და ნებისმიერი ზედმეტი ელემენტის შემთხვევაში ფეილდება; არქივის შემადგენლობასა
და CRC-საც ამოწმებს. Artifact ინახება 30 დღე. შეცდომა ჩანს Actions/PR checks-ში.
არსებული Slack notifier მხოლოდ `Validate KLAVA`-ს აკვირდება, არა ამ ახალ workflow-ს.

## ტესტების ფარგლები და პრაქტიკული შემოწმება

| დონე | მტკიცებულება / საზღვარი |
|---|---|
| ავტომატური რეგრესია | source/frozen ბილიკები, უცხო CWD, ქართული ბილიკი, BOM, ცარიელი/დაკარგული/არასწორად კოდირებული ფაილი, ორი ხაზის მინიმუმი, დაზიანების გარეშე ხელახალი ცდა, სწორი/არასწორი კლავიშები, SPACE, დასრულება და reload |
| რეალური Tk widgets | opt-in `tests/test_trainer_gui.py`, Windows Runner-ზე; პროგრამულად მიწოდებული keysym-ები, კლავიატურის 27 ელემენტი, ფერი და სესიის ციკლი |
| რეალური EXE | ZIP-იდან სხვა ქართულ/გამოტოვებიან ბილიკში ამოღება, უცხო CWD-დან გაშვება, KLAVA ფანჯრის სათაურის აღმოჩენა, პროცესის დასრულება და ორფაილიანი საქაღალდის გადამოწმება |
| ხელით ვიზუალური მიღება | ცალკე Windows 10/11 desktop-ზე ჯერ შესასრულებელია; ავტომატური გაშვება არ ადასტურებს შრიფტის, განლაგების, DPI-ის ან ფიზიკური კლავიატურის სრულ სისწორეს |

ადამიანის საბოლოო შემოწმება: გახსენით EXE, დაიწყეთ სავარჯიშო, აკრიფეთ სწორი და
არასწორი ასო და SPACE, დაასრულეთ ორი ხაზი, შეცვალეთ ფაილი და დაიწყეთ თავიდან.
შეამოწმეთ layout და ქართული ტექსტის ხილვადობა. მიმდინარე სესიის შეწყვეტა:
`Ctrl+Alt+Shift+Q`. სცადეთ დაკარგული, ცარიელი, ერთი ხაზის და არასწორი კოდირების ფაილი;
უნდა გამოჩნდეს შეცდომა და დარჩეს დაწყების შესაძლებლობა. ტესტი ჩაატარეთ ფაილის ასლზე.

## რისკები, დაბრუნება და HANDOFF

ეს არის unsigned x64 build; ხელმოწერა ამ სამუშაოში არ შედის. ზუსტი Windows 10/11
desktop თავსებადობა საბოლოო ხელით ტესტამდე არ ითვლება დადასტურებულად.
არსებული Accuracy/CPM/adaptation ხარვეზები პაკეტიზაციით არ გვარდება.
UI-ში უკვე არსებული SPACE-ის ვიზუალური თავისებურებები უცვლელია.

Rollback: დაბრუნდით წინა build-ზე, შეინახეთ თქვენი `exercises.txt` ცალკე ასლად.
წყაროს ცვლილებების დაბრუნება მოხდეს ჩვეულებრივი revert PR-ით; ისტორია არ გადაიწეროს.
სამუშაო შტო: `feat/windows-portable`; merge მხოლოდ მფლობელის ცალკე თანხმობით.
CI run-ისა და Artifact-ის ფაქტობრივი შედეგები დაფიქსირდება PR-ის ანგარიშში.
Drive mirror არ არის საჭირო: ეს GitHub-ის ტექნიკური პროცედურაა.

## შესრულების ჩანაწერი — 2026-10-28

- [PR #7](https://github.com/avtotrainer/klava/pull/7), build commit
  `36891865dc080032f6e73415f61ceab1186e1eb6`.
- [Windows run 40575875572](https://github.com/avtotrainer/klava/actions/runs/40575875572):
  წარმატება; 28 regression ტესტი, 1 ცალკე რეალური Tk ტესტი, PyInstaller აწყობა,
  ZIP/CRC შემოწმება და გადატანილი EXE-ის KLAVA ფანჯრის გაშვება გავიდა.
- [Linux validation](https://github.com/avtotrainer/klava/actions/runs/40575875385): წარმატება.
- [Build Artifact](https://github.com/avtotrainer/klava/actions/runs/40575875572/artifacts/12767716478):
  10,883,895 ბაიტი; მოქმედების ვადა 2026-11-26. GitHub-ის ჩამოტვირთვის გარე ZIP
  შეიცავს `KLAVA-windows-x64.zip`-ს; სწორედ შიდა გასავრცელებელ ZIP-შია ორი ფაილი.
- ლოკალურად pytest: 28 passed / 1 skipped (desktop არ იყო); Ruff, compileall და
  14 Markdown ფაილის ლოკალური ბმულების შემოწმება წარმატებულია.
- პირდაპირი `git push` ვერ შესრულდა HTTPS ავტორიზაციის არქონის გამო. GitHub
  connector-ით შეიქმნა commit და PR; remote tree SHA ზუსტად დაემთხვა ლოკალურ
  შემოწმებულ tree-ს: `76f64db9e58a05ee1574397a49a622dcacb952cf`.
- საწყის lint შემოწმებაზე აღმოჩენილი გამოუყენებელი import ამოღებულია; საბოლოო Ruff მწვანეა.
- არც main merge, არც Release, არც Drive mirror და არც Slack გაგზავნა შესრულებულა.
- შემდეგი მოქმედება: Windows 10/11 desktop-ზე ზემოთ მოცემული ხელით მიღების ტესტი;
  შემდეგ მფლობელის ცალკე გადაწყვეტილება PR #7-ის გაერთიანებაზე.

## მომხმარებლის პროფილის ინსტალატორი — 2026-10-28

მომხმარებლის დაზუსტებული მოთხოვნით მიმდინარე ინსტალატორია
`KLAVA-User-Setup-x64.exe`: ადმინისტრატორის უფლებების გარეშე, მხოლოდ მიმდინარე
Windows მომხმარებლისთვის. ეს ცვლის წინა Program Files ვარიანტს PR #8-ში.
Portable ZIP კვლავ ზუსტად ორი ფაილია; ინსტალირებულ ვარიანტს ემატება წაშლის ფაილები.

| კომპონენტი | მდებარეობა / ქცევა |
|---|---|
| პროგრამა | `%LOCALAPPDATA%\Programs\KLAVA\KLAVA.exe` |
| საწყისი ნიმუში | პროგრამის გვერდით `default-exercises.txt`; ინსტალირებული რეჟიმის მაჩვენებელიცაა |
| პირადი სავარჯიშოები | `%LOCALAPPDATA%\KLAVA\exercises.txt`; თითო Windows მომხმარებელს თავისი ასლი აქვს |
| გაშვება | Start → KLAVA → KLAVA |
| ტექსტის რედაქტირება | Start → KLAVA → Edit exercises; სისტემის `.txt` რედაქტორი |
| Desktop | არჩევითი მალსახმობი მხოლოდ მიმდინარე მომხმარებლისთვის |
| წაშლა | Windows Installed apps / Apps & features → KLAVA → Uninstall |

გაუშვით ინსტალატორი ჩვეულებრივი ორმაგი დაწკაპუნებით, **არა Run as administrator**.
`PrivilegesRequired=lowest` elevation-ს არ ითხოვს. პროგრამა, მალსახმობები და
Uninstall ჩანაწერი მომხმარებლის პროფილსა და HKCU-ში თავსდება; Program Files-ის,
HKLM-ის ან სისტემური უფლებების ცვლილება საჭირო არ არის.
პირადი სავარჯიშოები პროგრამის პირველი გაშვებისას იქმნება და ხელახალი დაყენებისას
თუ Uninstall-ისას არ იშლება. ცარიელი ან არასწორი კოდირების არსებული ფაილი არ
გადაიწერება. თუ პირადი ფაილი წაშლილია, შემდეგ გაშვებაზე საწყისი ნიმუში აღდგება.
ტექსტი შეინახეთ UTF-8 ფორმატით; მინიმუმ ორი ხაზი და ყოველი სესიის reload უცვლელია.

წინა Program Files ინსტალაცია ავტომატურად არ იშლება და არ იცვლება. ახალ
მომხმარებლის ინსტალაციას აქვს საკუთარი `AppId=KLAVA.CurrentUser`, რათა ძველი
სისტემური ინსტალაციის ბილიკი/Uninstall ჩანაწერი არ გადაიბაროს. ძველი ვარიანტის
წაშლა საჭიროების შემთხვევაში ადმინისტრატორმა უნდა შეასრულოს. სავარჯიშოების
მდებარეობა ორივე ვარიანტში იგივეა, ამიტომ არსებული პირადი ტექსტი შენარჩუნდება.
Portable ფაილის ტექსტის გადასატანად გამოიყენეთ „Edit exercises“-ით გახსნილი ფაილი.

სკოლის მიერ ცალკე დაწესებული AppLocker/WDAC ან სხვა პროგრამების გაშვების პოლიტიკა
ამ ინსტალატორით არ იცვლება: ასეთ გარემოში დაშვება ადმინისტრატორთან შეთანხმდება.
ეს მომხმარებლის უფლებებში დაყენებაა და არა ორგანიზაციული შეზღუდვების გვერდის ავლა.

### განხორციელება და შემოწმება

- `packaging/windows-installer.iss`: Inno Setup 6, non-admin ინსტალაცია,
  `%LOCALAPPDATA%\Programs`, HKCU Uninstall, პირადი Start/Desktop მალსახმობები.
- `logic/resources.py`: installed/portable/source გზები და პირადი ფაილის
  ექსკლუზიური შექმნა; არსებული ფაილი არ გადაიწერება.
- `main.py`: პირადი მონაცემების მომზადება და `--edit-exercises` მალსახმობი.
  `Trainer` რჩება სესიის კონტროლერად; სასწავლო ზღვრები და UI უცვლელია.
- `tests/test_installed.py`: პროფილების განცალკევება, საწყისი ასლი, შეცვლილი/
  ცარიელი/არასწორი ფაილის შენარჩუნება, რედაქტორის მალსახმობი და შეცდომის დიალოგი.
- `scripts/test_windows_installer.ps1`: რეალური install, HKCU რეგისტრაცია,
  shortcut target-ები, გაშვება, reinstall და uninstall; იცავს არსებულ ფაილებს.
- `scripts/test_standard_user_install.ps1`: მხოლოდ დროებით GitHub Windows Runner-ზე
  ქმნის სტანდარტულ, არაადმინისტრატორ ანგარიშს და იმავე ტესტს უშვებს მის პროფილში.
  ტესტის დასაწყისში მოწმდება, რომ პროცესს Administrator როლი არ აქვს.
  ანგარიშის იზოლირებულ გაშვებაში მოწმდება პროცესის სიცოცხლე და პირველი ფაილის
  შექმნა; ფანჯრის სათაურის აღმოჩენა ცალკე ჩვეულებრივ runner ტესტში სრულდება.
  ტესტის ანგარიში იშლება ბოლოს; რეალური სასკოლო ანგარიშები არ იცვლება.

Windows-ზე, PyInstaller build-ის შემდეგ, რეპოზიტორიის root-იდან PowerShell-ში:

```powershell
& "${env:ProgramFiles(x86)}\Inno Setup 6\ISCC.exe" packaging/windows-installer.iss
```

შედეგი: `dist/KLAVA-User-Setup-x64.exe`. CI კომპილატორის ვერსია ჩანს build log-ში;
byte-for-byte იდენტური build გარანტირებული არ არის. წარმატებული ტესტების შემდეგ
იტვირთება `KLAVA-user-installer-x64` Artifact (30 დღე). Release არ ქვეყნდება.

საფუძველი: [PrivilegesRequired](https://jrsoftware.org/ishelp/topic_setup_privilegesrequired.htm),
[Non-admin install mode](https://jrsoftware.org/ishelp/topic_admininstallmode.htm).

### HANDOFF და წინა მცდელობა

შტო `feat/windows-installer`, [PR #8](https://github.com/avtotrainer/klava/pull/8),
დამოკიდებულია ღია [PR #7](https://github.com/avtotrainer/klava/pull/7)-ზე.
არცერთი არ გაერთიანებულა. საწყისი installer commit:
`148402bc78014a44ee0b1f035be0d692e5d1f6a0`.
მისი [Program Files ტესტი](https://github.com/avtotrainer/klava/actions/runs/40628755681)
წარმატებული იყო, თუმცა მომხმარებელმა შემდეგ მოითხოვა non-admin დაყენება.
ამიტომ ძველი Artifact მიმდინარე ინსტალატორად აღარ გამოიყენოთ.

მიმდინარე საბოლოო run, commit და ჩამოტვირთვის ბმული ინახება PR #8-ის ანგარიშში.
ლოკალური რეგრესია: 36 passed, 1 GUI skipped; Ruff და compileall წარმატებულია.
დარჩენილი ხელით მიღება: Windows 10/11 GUI/DPI, ფიზიკური კლავიატურა, რედაქტორის
ასოციაცია და სკოლის რეალური მოწყობილობის პროგრამების გაშვების პოლიტიკა.
Rollback: პირადი Uninstall და წინა Portable build; საჭირო ტექსტი დააკოპირეთ
Portable `exercises.txt`-ში. Uninstall პირად სავარჯიშოებს არ შლის.

CI-ის პირველი non-admin მცდელობა ([run 40629647008](https://github.com/avtotrainer/klava/actions/runs/40629647008))
შეჩერდა ტესტის მომზადებაზე: ახალი ანგარიშისთვის `GetFolderPath` არსებულ საქაღალდეს
ეძებდა და ცარიელი LocalAppData დააბრუნა. ტესტის wrapper-ში დაემატა `Create`
ოფცია, რომელიც Windows-ს პირადი ცნობილი საქაღალდის შექმნას სთხოვს. ეს არ ცვლის
აპლიკაციის ან ინსტალატორის უფლებებს; ინსტალაციამდე შეჩერებული მცდელობა არ ითვლება
სტანდარტული მომხმარებლის წარმატებულ ტესტად.

`Create`-ით განმეორებამაც იგივე profile-preparation შეცდომა აჩვენა
([run 40629884019](https://github.com/avtotrainer/klava/actions/runs/40629884019)).
`Start-Process -Credential`-ზე დაფუძნებული wrapper ჩანაცვლდა დროებითი,
`RunLevel Limited` Task Scheduler გაშვებით: Windows თავად ქმნის მომხმარებლის
სესიასა და გარემოს, runner-ის გარემოს მემკვიდრეობით გადაცემის ნაცვლად.
ამ სატესტო დავალებას ტრიგერი/განრიგი არ აქვს და ბოლოს იშლება ანგარიშთან ერთად;
მომხმარებლის კომპიუტერზე ავტომატიზაცია არ იქმნება.

## KLV exercise library and dual-scope setup — 2026-10-28

**Working branch:** `feat/klv-selection-dual-installer`. This section describes the proposed, not yet merged, implementation.

- Each Windows user maintains their own library under `%LOCALAPPDATA%\\KLAVA`.
- Plain UTF-8 text exercises now use the `.klv` extension. Contents remain one typing line per line, minimum two nonblank lines.
- KLAVA creates `exercises.klv` on first run from the distributed seed; previously saved `exercises.txt` in that user's library is copied, never deleted.
- The File menu includes `სავარჯიშოს არჩევა`, listing only `.klv` files from the current user's library; selection is remembered in `selected-exercise.txt`.
- Installer offers **Current User** (no admin needed, `%LOCALAPPDATA%\\Programs\\KLAVA`) and **All Users** (administrative elevation, `%ProgramFiles%\\KLAVA`).
- Both choices install exactly the same executable and default seed, without modifying user data during setup or uninstall.
- Portable archive remains exactly two files: `KLAVA.exe` and `exercises.klv`. The first run copies the bundled `.klv` seed into the user's library.
- For noninteractive installations, `/CURRENTUSER` and `/ALLUSERS` explicitly set the scope.
- Machine-wide installation cannot bypass Windows administrative permissions or domain restrictions.
- CI verifies standard-user installation, per-user installation lifecycle, machine-wide installation/uninstall and portable ZIP shape. Results must be read from the run logs; configuration alone is not proof of success.

**Rollback:** uninstall executable via Windows Apps without removing `%LOCALAPPDATA%\\KLAVA`. Existing `exercises.txt` remains as a migration source. Keep backups when editing user content. The previous `.txt` portable file is not read by the new portable format except for a prior user-library migration.

### CI diagnostic follow-up — 2026-10-28

The dedicated Windows standard-user task previously exceeded its 180-second window in [run 40705931548](https://github.com/avtotrainer/klava/actions/runs/40705931548). The same run independently passed current-user installer lifecycle and all-users installation/uninstall; those checks do **not** prove non-admin execution in the isolated account. The last step now captures Task Scheduler state, last exit code, a progress marker and the temporary user's PowerShell transcript before reporting failure. These traces distinguish a task that never starts from a hanging installer or executable. No production user accounts or profiles are changed by this CI-only diagnostic update.

## Distribution decision — 2026-10-28

The owner discontinued the standalone portable distribution. The supported deliverable is now **KLAVA-Setup-x64.exe** only, with Current User and All Users options. GitHub Actions still builds an internal PyInstaller executable as the installer's input, but no longer assembles or uploads the two-file portable ZIP. Older portable archives may remain in historical CI artifacts; they are not the current deliverable. The standard-user integration test remains a separate unresolved gate until verified.

## Acceptance-gate decision — 2026-10-29

The project owner confirmed that the installer completed and KLAVA works on a real Windows administrator account. The isolated temporary standard-user GitHub Actions process remained a CI harness problem: the scheduler could not launch the task, and a direct credentialed launch lacked a normal LOCALAPPDATA profile. Rather than treating a GitHub runner account provisioning defect as an application regression, the fragile isolated-account stage has been removed from the **required** Windows Installer workflow. This does not constitute a pass for non-admin installations. That acceptance scenario remains **NOT VERIFIED** until it can run on an actual restricted Windows account with proper user-profile initialization. Existing Windows CI continues to test a real install/reinstall/uninstall in current-user mode and a real all-users install/uninstall, plus Python, GUI and build checks.

Release status is **pending**. No code signing; unsigned warning is expected. No PR merging or public GitHub Release is included in this change.
