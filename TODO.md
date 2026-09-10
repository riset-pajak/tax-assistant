# TODO - Tuntunan Pengembangan

## Status

- [ ] Belum dimulai
- [O] Sedang dikerjakan
- [V] Selesai dan teruji
- [X] Diblokir

## Prinsip Pengembangan

1. Correctness > reproducibility > observability > performance > feature breadth.
2. Implementasikan perubahan secara kecil, bertahap, dan dapat diuji.
3. Web adalah satu-satunya kanal interaksi pengguna.
4. Google ADK melakukan orkestrasi; tool menjalankan operasi.
5. PostgreSQL dengan pgvector adalah primary vector store.
6. Operasi RAG database berada di service/repository, bukan di prompt atau agent logic.
7. Ollama menyediakan embedding, reranking, dan LLM inference dari compute plane.
8. Jangan mengganti model atau teknologi secara diam-diam.
9. Grounded generation wajib memakai evidence hasil retrieval.
10. Jika evidence tidak cukup, jawaban harus menyatakan ketidakcukupan evidence.
11. Jangan menyimpan IP, credential, secret, atau `.env` produksi di repository.
12. Docker-first deployment, tetapi hindari fragmentasi microservice yang tidak perlu pada MVP.

## Definition of Ready

Sebelum pekerjaan dimulai:

- [ ] Tujuan dan ruang lingkup jelas.
- [ ] Risiko dan dampak telah diidentifikasi.
- [ ] Dependency telah diperiksa.
- [ ] Rencana pengujian tersedia.
- [ ] Dokumentasi yang terpengaruh telah ditentukan.

## Definition of Done

Sebelum pekerjaan dinyatakan selesai:

- [ ] Implementasi selesai dan mengikuti architecture rules.
- [ ] Tidak ada hard-coded IP, credential, secret, atau environment-specific path.
- [ ] Unit test atau integration test tersedia sesuai tingkat risiko.
- [ ] Error handling dan timeout diterapkan.
- [ ] Logging dan audit mencatat informasi operasional yang diperlukan.
- [ ] Dokumentasi diperbarui jika diperlukan.
- [ ] Perubahan dapat dijalankan melalui dokumentasi atau Docker Compose.
- [ ] Perubahan telah diuji pada lingkungan yang sesuai.

---

## P0 - Infrastruktur dan Baseline Repository

- [ ] Buat struktur aplikasi sesuai `AGENTS.md`:
  - [ ] `app/agent`
  - [ ] `app/tools`
  - [ ] `app/services`
  - [ ] `app/rag`
  - [ ] `app/database`
  - [ ] `app/api`
  - [ ] `frontend`
  - [ ] `tests`
  - [ ] `scripts`
  - [ ] `docker`
  - [ ] `config`
- [ ] Tetapkan struktur package/backend dan konfigurasi aplikasi.
- [ ] Buat `docker-compose.yml` untuk PostgreSQL, pgvector, Ollama, dan aplikasi.
- [ ] Buat `.env.example` tanpa nilai rahasia.
- [ ] Tambahkan configuration loader yang membaca environment.
- [ ] Siapkan database migration dan schema initialization.
- [ ] Tambahkan script validasi infrastruktur.
- [ ] Tambahkan baseline unit tests dan integration tests.
- [ ] Tambahkan linting, formatting, dan build checks.
- [ ] Tambahkan workflow CI dasar.
- [ ] Perbarui dokumentasi struktur repository.

**Acceptance Criteria P0**

- [ ] Repository dapat dibangun dari kondisi bersih.
- [ ] Database dapat dibuat dan dimigrasikan secara otomatis.
- [ ] Unit tests dan integration tests dasar lulus.
- [ ] Dokumentasi menyatakan cara menjalankan aplikasi.
- [ ] Tidak ada secret atau IP hardcoded.

---

## P1 - Konektivitas Control Plane dan Compute Plane

- [ ] Konfigurasikan koneksi control plane ke Ollama menggunakan environment variable.
- [ ] Implementasikan Ollama client dengan timeout, retry, dan error mapping.
- [ ] Buat health check untuk aplikasi dan Ollama.
- [ ] Validasi model embedding melalui Ollama.
- [ ] Validasi model reranker melalui Ollama.
- [ ] Validasi model LLM melalui Ollama.
- [ ] Verifikasi bahwa model yang dipakai kompatibel dengan runtime Ollama.
- [ ] Jangan mengganti baseline model tanpa ADR atau persetujuan.
- [ ] Tambahkan integration test untuk Ollama connectivity.
- [ ] Dokumentasikan model baseline dan metode validasinya.

**Acceptance Criteria P1**

- [ ] Control plane dapat menghubungi Ollama melalui compute plane.
- [ ] Browser tidak dapat mengakses Ollama secara langsung.
- [ ] Konektivitas model embedding, reranker, dan LLM telah diverifikasi.
- [ ] Failure pada Ollama tidak menyebabkan crash tak terkendali.
- [ ] Status model dan koneksi dapat diperiksa melalui health endpoint.

---

## P2 - Knowledge Ingestion

- [ ] Tentukan format dan sumber dokumen yang didukung.
- [ ] Implementasikan document parser.
- [ ] Implementasikan structural chunking untuk dokumen terstruktur.
- [ ] Pertahankan hierarchy dan metadata dokumen.
- [ ] Validasikan hasil parsing dan chunking.
- [ ] Implementasikan embedding pipeline melalui Ollama.
- [ ] Simpan metadata sumber, identifier, versi, dan timestamp.
- [ ] Implementasikan idempotent upsert untuk dokumen dan chunk.
- [ ] Tambahkan retry dan handling untuk partial failure.
- [ ] Catat ingestion activity ke SQLite audit log.
- [ ] Tambahkan command atau API untuk ingest dokumen.
- [ ] Tambahkan integration test ingestion.

**Acceptance Criteria P2**

- [ ] Dokumen dapat diparse menjadi chunk yang dapat diretrieval.
- [ ] Metadata sumber tetap melekat pada setiap chunk.
- [ ] Ingestion ulang tidak membuat duplikasi tak terkendali.
- [ ] Error ingestion tercatat dan dapat ditelusuri.
- [ ] Embedding dilakukan melalui Ollama, bukan di control plane.

---

## P3 - Semantic Retrieval dengan pgvector

- [ ] Implementasikan repository layer untuk PostgreSQL dan pgvector.
- [ ] Implementasikan primary interface:

```python
search_knowledge(query: str, top_k: int = 5)
```

- [ ] Buat query embedding melalui Ollama.
- [ ] Lakukan semantic search menggunakan pgvector.
- [ ] Terapkan metadata filtering sesuai kebutuhan.
- [ ] Batasi hasil pencarian berdasarkan `top_k`.
- [ ] Normalisasikan atau validasikan hasil similarity.
- [ ] Pisahkan service layer dari database operation.
- [ ] Tambahkan unit test untuk query construction.
- [ ] Tambahkan integration test dengan PostgreSQL/pgvector.
- [ ] Tambahkan benchmark retrieval sederhana.

**Acceptance Criteria P3**

- [ ] `search_knowledge` mengembalikan chunk sesuai query.
- [ ] Retrieval dapat diuji tanpa ADK atau LLM.
- [ ] Hasil retrieval membawa metadata sumber yang diperlukan.
- [ ] Database operation tidak berada di prompt atau agent logic.
- [ ] Retrieval berhasil pada dataset uji yang telah ditentukan.

---

## P4 - Reranking

- [ ] Terima candidate chunks dari pgvector retrieval.
- [ ] Implementasikan reranker service melalui Ollama.
- [ ] Validasi input dan output model reranker.
- [ ] Gabungkan hasil reranking dengan metadata sumber.
- [ ] Terapkan threshold atau mekanisme penolakan hasil relevan rendah.
- [ ] Jangan melakukan fallback ke model lain secara diam-diam.
- [ ] Tambahkan unit test untuk adapter reranker.
- [ ] Tambahkan integration test untuk Ollama reranking.
- [ ] Ukur dampak reranking terhadap kualitas retrieval.

**Acceptance Criteria P4**

- [ ] Candidate chunks dapat direrank secara independen.
- [ ] Hasil akhir memiliki ranking yang dapat dijelaskan.
- [ ] Reranker dijalankan melalui compute plane.
- [ ] Kegagalan reranker ditangani secara eksplisit.
- [ ] Tidak ada silent model substitution.

---

## P5 - Google ADK Integration

- [ ] Susun agent configuration untuk Google ADK.
- [ ] Definisikan tool boundary dengan schema yang jelas.
- [ ] Hubungkan ADK dengan `search_knowledge`.
- [ ] Pastikan database operation berada di service/repository.
- [ ] Tambahkan validation untuk argument tool.
- [ ] Tambahkan timeout dan error mapping untuk tool.
- [ ] Tambahkan structured error response.
- [ ] Catat tool execution ke audit log.
- [ ] Tambahkan unit test untuk ADK tool.
- [ ] Tambahkan integration test ADK dengan dependency mock.

**Acceptance Criteria P5**

- [ ] ADK dapat memanggil RAG tool melalui service layer.
- [ ] Tool boundary jelas dan tidak mengekspos operasi internal.
- [ ] Error tool tidak bocor sebagai traceback mentah.
- [ ] Agent tetap berjalan ketika satu tool gagal.
- [ ] Tool dapat diuji secara independen.

---

## P6 - Grounded Generation

- [ ] Implementasikan context assembly dari chunk hasil reranking.
- [ ] Buat prompt template untuk grounded generation.
- [ ] Kirim context dan pertanyaan ke Ollama LLM.
- [ ] Pastikan evidence menjadi sumber kebenaran utama.
- [ ] Terapkan instruksi untuk tidak mengarang fakta.
- [ ] Terapkan respons ketika evidence tidak cukup.
- [ ] Tambahkan batas panjang context.
- [ ] Tambahkan timeout dan retry yang aman.
- [ ] Tambahkan unit test untuk context assembly.
- [ ] Tambahkan integration test generation dengan fixture.

**Acceptance Criteria P6**

- [ ] Jawaban LLM hanya didasarkan pada evidence yang diberikan.
- [ ] Jawaban untuk pertanyaan tanpa evidence tidak mengarang fakta.
- [ ] Context assembly dapat diuji tanpa memanggil LLM.
- [ ] Error dari Ollama ditangani secara terstruktur.
- [ ] Generation dapat diuji secara deterministik dengan fixture.

---

## P7 - Citation dan Source Presentation

- [ ] Tentukan struktur citation yang stabil.
- [ ] Hubungkan setiap jawaban dengan source identifier.
- [ ] Tampilkan judul, sumber, lokasi chunk, dan metadata terkait.
- [ ] Pastikan citation berasal dari retrieved evidence.
- [ ] Jangan membuat citation dari hasil generative model.
- [ ] Tambahkan mekanisme verifikasi citation oleh frontend.
- [ ] Tambahkan unit test untuk citation assembly.
- [ ] Tambahkan integration test untuk citation propagation.

**Acceptance Criteria P7**

- [ ] Setiap factual answer memiliki citation yang dapat ditelusuri.
- [ ] Citation tidak berasal dari hallucination LLM.
- [ ] Sumber dapat dibuka atau diverifikasi oleh pengguna.
- [ ] Metadata citation tidak hilang antar-layer.
- [ ] Jawaban tanpa sumber tidak ditandai sebagai grounded.

---

## P8 - Web UI

- [ ] Bangun halaman percakapan utama.
- [ ] Hubungkan frontend ke Python API.
- [ ] Tampilkan pertanyaan, jawaban, loading state, dan error state.
- [ ] Tampilkan citation di dekat factual answer.
- [ ] Tambahkan kemampuan membuka atau memeriksa sumber.
- [ ] Pastikan frontend tidak memanggil Ollama secara langsung.
- [ ] Tambahkan accessibility dasar.
- [ ] Tambahkan protection terhadap XSS dan HTML yang tidak terpercaya.
- [ ] Tambahkan handling untuk stream atau response non-streaming.
- [ ] Tambahkan integration test frontend.

**Acceptance Criteria P8**

- [ ] Pengguna dapat bertanya melalui browser dan menerima jawaban.
- [ ] Web hanya berinteraksi melalui backend yang sah.
- [ ] Citation terlihat dan dapat diverifikasi.
- [ ] Error tidak menampilkan secret atau traceback internal.
- [ ] UI dapat digunakan pada kondisi koneksi gagal.

---

## P9 - Agentic RAG

- [ ] Rencanakan query reformulation.
- [ ] Rencanakan retrieval retry dengan budget yang terbatas.
- [ ] Tambahkan strategi deduplikasi hasil retry.
- [ ] Batasi jumlah retry dan waktu eksekusi.
- [ ] Jangan membiarkan agent mengubah evidence secara bebas.
- [ ] Tambahkan perlindungan terhadap prompt injection.
- [ ] Tambahkan unit test untuk reformulation dan retry.
- [ ] Tambahkan integration test untuk agentic retrieval flow.
- [ ] Bandingkan hasil agentic RAG dengan baseline RAG.

**Acceptance Criteria P9**

- [ ] Query reformulation tidak menghilangkan intent pengguna.
- [ ] Retrieval retry memiliki batas yang jelas.
- [ ] Agent tidak melakukan loop tanpa batas.
- [ ] Evidence tetap utuh dan dapat dicantumkan.
- [ ] Kualitas retrieval tidak menurun dibandingkan baseline.

---

## P10 - Evaluasi dan Observability

- [ ] Buat evaluation dataset untuk domain pajak.
- [ ] Tambahkan evaluasi retrieval: recall, precision, atau metrik relevan.
- [ ] Tambahkan evaluasi grounded generation.
- [ ] Tambahkan evaluasi citation correctness.
- [ ] Tambahkan log operasional ke SQLite.
- [ ] Tambahkan request, agent, tool, dan retrieval correlation ID.
- [ ] Tambahkan metrics untuk latency, error, dan usage.
- [ ] Pastikan log tidak menyimpan secret atau data sensitif yang tidak diperlukan.
- [ ] Tambahkan dashboard atau laporan evaluasi.
- [ ] Tambahkan regression test untuk perubahan RAG penting.

**Acceptance Criteria P10**

- [ ] Setiap komponen RAG memiliki test yang independen.
- [ ] Retrieval, reranking, context assembly, ADK tool, Ollama, API, dan frontend teruji.
- [ ] Perubahan kualitas dapat dideteksi melalui evaluasi.
- [ ] Masalah operasional dapat ditelusuri melalui log dan correlation ID.
- [ ] Data sensitif tidak bocor melalui log atau UI.

---

## P11 - Additional Tools dan Multi-Agent

- [ ] Identifikasi kebutuhan tool tambahan dari使用 kasus nyata.
- [ ] Buat ADR sebelum menambahkan tool atau agent baru.
- [ ] Tambahkan tool dengan schema, validation, dan error handling.
- [ ] Pisahkan tanggung jawab antar-agent.
- [ ] Batasi komunikasi antar-agent dengan interface terstruktur.
- [ ] Tambahkan test untuk setiap tool dan agent.
- [ ] Evaluasi kebutuhan multi-agent sebelum implementasi.
- [ ] Dokumentasikan alasan, batasan, dan trade-off arsitektur.

**Acceptance Criteria P11**

- [ ] Tool baru tidak merusak baseline RAG.
- [ ] Multi-agent hanya digunakan jika memberi manfaat terukur.
- [ ] Setiap agent memiliki tanggung jawab yang jelas.
- [ ] ADR tersedia untuk keputusan arsitektur penting.
- [ ] Tool dan agent dapat diuji secara independen.

---

## Cross-Cutting Checklist

### Security

- [ ] Gunakan environment variables dan `.env.example`.
- [ ] Jangan commit secret atau production `.env`.
- [ ] Validasi semua input pengguna.
- [ ] Batasi ukuran dokumen dan chunk.
- [ ] Terapkan timeout untuk semua external call.
- [ ] Redaksi secret dan data sensitif dari log.
- [ ] Lindungi API dari akses tidak sah.
- [ ] Gunakan HTTPS pada deployment produksi.
- [ ] Terapkan least privilege untuk database dan service account.

### Database

- [ ] Gunakan migration yang dapat diulang dan dapat di-rollback.
- [ ] Gunakan foreign key dan constraint yang sesuai.
- [ ] Pertahankan metadata sumber dan versi dokumen.
- [ ] Verifikasi schema pgvector.
- [ ] Uji backup dan restore.
- [ ] Catat audit log ke SQLite sesuai kebutuhan.

### Deployment

- [ ] Dokumentasikan cara menjalankan development.
- [ ] Dokumentasikan cara menjalankan production.
- [ ] Gunakan Docker-first deployment.
- [ ] Pisahkan konfigurasi development, staging, dan production.
- [ ] Tambahkan health dan readiness checks.
- [ ] Tambahkan graceful shutdown.
- [ ] Tambahkan prosedur rollback.
- [ ] Tambahkan prosedur rotasi secret.

### Documentation

- [ ] Perbarui `README.md`.
- [ ] Perbarui `docs/ARCHITECTURE.md`.
- [ ] Perbarui `docs/INFRASTRUCTURE.md`.
- [ ] Perbarui `docs/RAG.md`.
- [ ] Perbarui `docs/TESTING.md`.
- [ ] Tambahkan ADR untuk perubahan arsitektur penting.
- [ ] Tambahkan runbook operasional.

---

## Urutan Eksekusi yang Disarankan

1. Selesaikan P0.
2. Validasi P1 sebelum membangun RAG.
3. Bangun ingestion, retrieval, dan reranking sebelum integrasi ADK.
4. Implementasikan grounded generation dan citation.
5. Hubungkan Web UI.
6. Tambahkan agentic RAG setelah baseline stabil.
7. Tambahkan evaluasi dan observability.
8. Tambahkan tool atau multi-agent hanya setelah kebutuhan terbukti.

## Release Gate

Sebelum release:

- [ ] Semua fase wajib telah diuji.
- [ ] Tidak ada test penting yang gagal.
- [ ] Model baseline telah diverifikasi pada runtime Ollama.
- [ ] Database migration dan backup telah diuji.
- [ ] Security checklist telah dipenuhi.
- [ ] Dokumentasi deployment telah diperbarui.
- [ ] Known issues dan workaround telah didokumentasikan.