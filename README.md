# Sor Terminal Assistant

`sor` terminalda sual verməyə və Codex-dən cavab almağa imkan verir. Cavab üçün yazılan sualla yanaşı, həmin terminal sessiyasının əvvəlki komandaları və görünən nəticələri də göndərilir.

```bash
sor "Bu xətanın səbəbi nədir?"
```

Sual yazılmadan `sor` çağırıldıqda son tamamlanan komandanı izah edir. Əsas
rejimlər:

```bash
sor                 # son komandanı izah et
sor fix              # problemi izah et və düzəldilmiş əmri təklif et
sor cmd "portu göstər" # yalnız shell əmri qaytar
sor deep "bu xəta niyə baş verir?" # Luna high ilə daha dərin təhlil
sor --last 5 "nə baş verdi?"
sor --no-context "tar nə edir?"
```

Təklif olunan əmrlər avtomatik icra edilmir.

Sessiya idarəsi:

```bash
sor --status
sor pause
sor resume
sor clear
```

## İş prinsipi

- İkinci Codex hesabının lokal `app-server` daemon-una qoşulur.
- `gpt-6-luna` modelini `low` reasoning səviyyəsində işlədir.
- `deep` rejimi eyni modeli `high` reasoning səviyyəsində işlədir.
- Modelin ilk mətni gələnədək terminalda fəaliyyət göstəricisi göstərir.
- Hər sual üçün müvəqqəti, yalnız oxuma icazəli sessiya başladır.
- Hər VTE Bash sessiyasını ayrıca faylda saxlayır və komandaları exit code,
  qovluq və müddətlə birlikdə strukturlaşdırılmış formada qeyd edir. Qovluq
  `$XDG_RUNTIME_DIR/sor-sessions` altında, bu dəyişən yoxdursa cari istifadəçi
  üçün `/tmp` altında yaradılır.
- Sessiya qovluğu `0700`, log faylları `0600` icazəsi ilə yaradılır. Terminal bağlananda onun log faylı silinir.
- Adi sorğularda sessiyanın təmizlənmiş son 10 000 simvolunadək hissəsi
  göndərilir. `deep` rejimində limit 60 000 simvoldur.
- Bearer tokenləri, həssas environment dəyişənləri, tanınan GitHub/OpenAI
  tokenləri və private key blokları modelə göndərilməzdən əvvəl `[REDACTED]`
  ilə əvəz olunur. Xam lokal log dəyişdirilmir.

Recorder terminalın PTY çıxışını yazır; interaktiv shell-in ekranda göstərdiyi
komandalar da buna daxildir. VTE Bash başlanğıc hook-u recorder-i avtomatik
başladır. Bəzi `HISTCONTROL` qaydaları və prompt göstərilmədən shell-dən çıxış
son komandanın strukturlaşdırılmış qeydinin yaranmasına mane ola bilər.

## Tələblər

- Linux və Bash. Avtomatik qeyd üçün VTE əsaslı terminal lazımdır.
- ChatGPT hesabı ilə daxil olunmuş Codex CLI və işləyən app-server daemon.
- Python 3 və `websockets` paketi.
- Mövcud quraşdırma premium Codex qovluğu kimi `/home/fadayat/.codex-account-2`, Codex CLI kimi `/home/fadayat/.local/bin/codex` istifadə edir.

## Quraşdırma

```bash
mkdir -p "$HOME/.local/bin" "$HOME/.bashrc.d"
install -m 0755 bin/sor "$HOME/.local/bin/sor"
install -m 0755 bin/sor-session-recorder "$HOME/.local/bin/sor-session-recorder"
install -m 0755 bin/sor-session-event "$HOME/.local/bin/sor-session-event"
install -m 0644 bash/sor-session.bash "$HOME/.bashrc.d/sor-session.bash"
```

`~/.bashrc` faylı `~/.bashrc.d` qovluğundakı faylları oxumalıdır. Sonra yeni terminal aç və yoxla:

```bash
sor --status
sor "Salam, necəsən?"
```

## Fayllar

- `bin/sor` — lokal app-server socket-i ilə Codex-ə sual göndərir.
- `bin/sor-session-recorder` — PTY vasitəsilə bir terminal sessiyasını qeyd edir.
- `bin/sor-session-event` — tamamlanan Bash komandalarının metadatasını yazır.
- `bash/sor-session.bash` — interaktiv VTE Bash sessiyalarında recorder-i başladır.

Gələcək provayder və versiya planı [ROADMAP.md](ROADMAP.md) faylındadır.
