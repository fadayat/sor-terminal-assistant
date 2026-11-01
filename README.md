# Sor Terminal Assistant

`sor` terminalda sual verməyə və Codex-dən cavab almağa imkan verir. Cavab üçün yazılan sualla yanaşı, həmin terminal sessiyasının əvvəlki komandaları və görünən nəticələri də göndərilir.

```bash
sor "Bu xətanın səbəbi nədir?"
```

`sor --status` terminal kontekstinin aktiv olub-olmadığını göstərir.

## İş prinsipi

- İkinci Codex hesabının lokal `app-server` daemon-una qoşulur.
- `gpt-6-luna` modelini `low` reasoning səviyyəsində işlədir.
- Hər sual üçün müvəqqəti, yalnız oxuma icazəli sessiya başladır.
- Hər VTE Bash sessiyasını ayrıca faylda saxlayır. Qovluq `$XDG_RUNTIME_DIR/sor-sessions` altında, bu dəyişən yoxdursa cari istifadəçi üçün `/tmp` altında yaradılır.
- Sessiya qovluğu `0700`, log faylları `0600` icazəsi ilə yaradılır. Terminal bağlananda onun log faylı silinir.
- Modelə sessiyanın təmizlənmiş son 60 000 simvolunadək hissəsi göndərilir. Buraya komandalar və nəticələr daxildir.

Recorder terminal girişini və çıxışını yazır. VTE Bash başlanğıc hook-u bunu avtomatik başladır. Digər terminal və shell-lərdə `sor-session-recorder` əmrini birbaşa işlətmək olar.

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
- `bash/sor-session.bash` — interaktiv VTE Bash sessiyalarında recorder-i başladır.
