# Sor inkişaf planı

Sor mərhələli hazırlanır. Erkən versiyalarda məqsəd bütün mümkün funksiyaları
bir dəfəyə əlavə etmək deyil; təhlükəsiz, test edilə bilən və yeni model
provayderlərinə açıq təməl qurmaqdır.

## Arxitektura istiqaməti

```text
terminal sessiyası
  -> kontekst toplayıcı
  -> məxfilik və seçim qatı
  -> sorğu rejimi
  -> provayder adapteri
  -> model cavabı
```

- **Kontekst toplayıcı** komanda, çıxış, exit code, qovluq və müddət kimi
  terminal məlumatlarını hazırlayır.
- **Məxfilik qatı** yalnız lazım olan konteksti seçir və ehtimal olunan
  sirləri modelə göndərməzdən əvvəl gizlədir.
- **Sorğu rejimi** `ask`, `fix`, `cmd` və `deep` kimi davranışları müəyyən edir.
- **Provayder adapteri** autentifikasiya, model seçimi və cavab axınını CLI
  məntiqindən ayırır. İlk adapter lokal Codex app-server üçündür.

## v0.2 — təhlükəsiz terminal təməli

- Strukturlaşdırılmış komanda metadatası.
- Sual yazılmadıqda son əmrin avtomatik izahı.
- `fix`, `cmd` və `deep` rejimləri.
- `--last`, `--no-context`, `pause`, `resume` və `clear` idarəsi.
- Modelə göndərilməzdən əvvəl secret redaction.
- Unit testlər və quraşdırma yoxlaması.
- Cari Codex 2 bağlantısının mərkəzləşdirilmiş konfiqurasiyası.

## v0.3 — sessiya və gündəlik istifadə

- Hər terminal üçün davam edən söhbət və `reset`.
- Təklif olunan əmri Bash sətrinə yerləşdirmək; avtomatik icra etməmək.
- Qısa yol, rəngli çıxış və daha aydın xəta mesajları.
- `doctor` komandası və sadə installer/updater.
- Konfiqurasiya faylı və provayder adapter interfeysi.

## v0.4 — çoxprovayderli işləmə

- Əlavə Codex hesabları və profilləri.
- İstifadəçinin gətirdiyi uyğun API və abunəlik inteqrasiyaları.
- Lokal model adapteri, məsələn Ollama.
- Rejimə görə provayder/model seçimi və təhlükəsiz fallback.
- Heç bir tokeni repo və ya terminal kontekstində saxlamayan credential qatı.

Hər inteqrasiya yalnız həmin xidmətin rəsmi olaraq icazə verdiyi autentifikasiya
üsulu ilə əlavə olunacaq. Bir xidmətin abunəliyi avtomatik olaraq ümumi API
açarı hesab edilməyəcək.

## v0.5 — zəngin kontekst

- Fayl, şəkil və clipboard girişi.
- Git və layihə kontekstinin seçimli əlavə edilməsi.
- Bash-dan əlavə Zsh və Fish dəstəyi.
- Kontekst büdcəsi, lokal məxfilik görünüşü və audit məlumatı.

## v1.0 meyarları

- Stabil CLI müqaviləsi və geriyə uyğun konfiqurasiya.
- Provayder xətalarının təhlükəsiz bərpası.
- Quraşdırma, yeniləmə və silmə axınları.
- Bash/Zsh/Fish üzrə inteqrasiya testləri.
- Sirlərin təsadüfən göndərilməsinə qarşı sənədləşdirilmiş təhlükəsizlik modeli.
