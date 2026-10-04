import os
import csv
import itertools
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from client_lib import download_file, upload_file

# ——— Konfigurasi ———
server_models = ['mt', 'mp']
ops           = ['download', 'upload']
volumes       = {
    '10MB':  'test_10MB.bin',
    '50MB':  'test_50MB.bin',
    '100MB': 'test_100MB.bin',
}
client_pools  = [1, 5, 50]
server_pools  = [1, 5, 50]
output_csv    = 'results_auto.csv'
# Ukuran batch maksimal ketika client > 10 dan client > server
BATCH_SIZE = 10
# ————————————————————

# Buat list semua kombinasi skenario
all_combos = list(itertools.product(
    server_models, ops, volumes, client_pools, server_pools
))

# 1) Inisialisasi atau baca CSV lama
rows = []
if os.path.exists(output_csv):
    with open(output_csv, newline='') as f:
        reader = csv.reader(f)
        rows = list(reader)
    if len(rows) > 1:
        print("=== Previous results from results_auto.csv ===")
        print(" | ".join(rows[0]))
        for data_row in rows[1:]:
            print(" | ".join(data_row))
        print(f"=== {len(rows)-1} scenarios already completed ===\n")
else:
    # buat file dan header baru
    header = [
        'No', 'ServerModel', 'Operation', 'Volume',
        'ClientPool', 'ServerPool',
        'TimePerClient(s)', 'Throughput(bytes/s)',
        'ClientOK', 'ClientFail', 'ServerOK', 'ServerFail'
    ]
    with open(output_csv, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
    rows = [header]

# 2) Tentukan dari skenario ke berapa melanjutkan
if len(rows) <= 1:
    start_idx = 0
else:
    processed = []
    for r in rows[1:]:
        try:
            processed.append(int(r[0]))
        except:
            pass
    start_idx = max(processed) if processed else 0

# 3) Loop skenario
for combo_index in range(start_idx, len(all_combos)):
    idx = combo_index + 1
    server_model, op, vol, csz, ssz = all_combos[combo_index]

    print(f"\n=== Scenario {idx}: SERVER={server_model.upper()} | "
          f"OP={op.upper()} | VOL={vol} | CLIENTS={csz} | SERVERS={ssz} ===")

    # spin up server
    server_script = 'server_mt_pool.py' if server_model == 'mt' else 'server_mp_pool.py'
    srv_proc = subprocess.Popen([
        'python', server_script, '--workers', str(ssz)
    ])
    time.sleep(3)  # tunggu server siap

    # pilih fungsi client
    func = download_file if op == 'download' else upload_file
    fname = volumes[vol]

    success = 0
    total_bytes = 0
    start_time = time.time()

    def client_task(i):
        t0 = time.time()
        try:
            ok, info = func(fname)
        except Exception as e:
            print(f"  [Client {i+1}/{csz}] ERROR – {e}")
            return False, 0
        dur = time.time() - t0
        transferred = info if (ok and op == 'download') else (os.path.getsize(fname) if ok else 0)
        status = 'OK' if ok else 'FAIL'
        print(f"  [Client {i+1}/{csz}] {status} – {dur:.2f}s")
        return ok, transferred

    # tentukan concurrency
    if csz > BATCH_SIZE and csz > ssz:
        max_workers = BATCH_SIZE
    else:
        max_workers = min(csz, ssz)

    # jalankan client dengan ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = [pool.submit(client_task, i) for i in range(csz)]
        for fut in as_completed(futures):
            ok, b = fut.result()
            if ok:
                success += 1
                total_bytes += b

    total_time = time.time() - start_time
    throughput = total_bytes / total_time if total_time > 0 else 0
    client_fail = csz - success

    # shutdown server
    srv_proc.terminate()
    srv_proc.wait()

    # tampilkan dan catat hasil
    print(f"--- Scenario {idx} complete: TotalTime={total_time:.2f}s | "
          f"Throughput={int(throughput)} B/s | Success={success}/{csz} ---")

    with open(output_csv, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            idx, server_model, op, vol,
            csz, ssz,
            f"{total_time:.2f}", int(throughput),
            success, client_fail,
            success, client_fail
        ])

print(f"\nAll done! Results saved to {output_csv}")
