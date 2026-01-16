# Load kamus kata dasar
def load_kamus():
    try:
        with open('kamus.txt', 'r', encoding='utf-8') as f:
            return set(line.strip().lower() for line in f if line.strip())
    except FileNotFoundError:
        print("Warning: kamus.txt tidak ditemukan. Stemming tanpa validasi kamus.")
        return set()

# Inisialisasi kamus
KAMUS = load_kamus()

def stemming_ays(word):
    """
    Algoritma stemming AYS dengan validasi kamus kata dasar
    untuk mengurangi over-stemming dan under-stemming
    """
    original_word = word
    word = word.lower()
    
    # Jika sudah kata dasar, langsung return
    if word in KAMUS:
        return word
    
    prefixes = [
        'meng', 'meny', 'men', 'mem', 'me',
        'peng', 'pen', 'pem', 'pe',
        'ber', 'per', 'di', 'ke', 'se', 'ter'
    ]
    
    suffixes = ['kan', 'an', 'i', 'lah', 'kah', 'nya']
    
    # Coba hilangkan suffix dulu
    temp_word = word
    removed_suffix = None
    for s in suffixes:
        if temp_word.endswith(s):
            temp_word = temp_word[:-len(s)]
            removed_suffix = s
            break
    
    # Cek apakah hasil setelah hilangkan suffix ada di kamus
    if temp_word in KAMUS:
        return temp_word
    
    # Coba hilangkan prefix dari hasil setelah suffix dihilangkan
    for p in prefixes:
        if temp_word.startswith(p):
            result = temp_word[len(p):]
            # Validasi: hasil harus ada di kamus atau minimal 3 karakter
            if result in KAMUS:
                return result
            # Jika tidak di kamus tapi hasil > 2 karakter, coba tetap gunakan
            if len(result) > 2:
                return result
    
    # Jika tidak berhasil dengan urutan suffix->prefix, coba prefix->suffix
    temp_word = word
    for p in prefixes:
        if temp_word.startswith(p):
            temp_word = temp_word[len(p):]
            break
    
    # Cek hasil setelah hilangkan prefix
    if temp_word in KAMUS:
        return temp_word
    
    # Hilangkan suffix dari hasil prefix
    for s in suffixes:
        if temp_word.endswith(s):
            result = temp_word[:-len(s)]
            if result in KAMUS:
                return result
            if len(result) > 2:
                return result
    
    # Jika semua gagal, return hasil terakhir yang valid atau kata asli
    # Hindari over-stemming dengan memastikan hasil minimal 3 karakter
    if len(temp_word) >= 3:
        return temp_word
    else:
        return word

def stemming_ays_detailed(word):
    """
    Algoritma stemming AYS dengan detail proses untuk debugging
    Returns: dict dengan informasi lengkap proses stemming
    """
    original_word = word
    word = word.lower()
    
    process_steps = []
    removed_prefix = None
    removed_suffix = None
    in_dictionary = False
    
    # Step 1: Cek apakah sudah kata dasar
    if word in KAMUS:
        process_steps.append(f"✓ Kata '{word}' ditemukan di kamus (sudah kata dasar)")
        return {
            'original': original_word,
            'result': word,
            'prefix_removed': None,
            'suffix_removed': None,
            'in_dictionary': True,
            'steps': process_steps
        }
    
    process_steps.append(f"• Kata '{word}' tidak ada di kamus, mulai proses stemming")
    
    prefixes = [
        'meng', 'meny', 'men', 'mem', 'me',
        'peng', 'pen', 'pem', 'pe',
        'ber', 'per', 'di', 'ke', 'se', 'ter'
    ]
    
    suffixes = ['kan', 'an', 'i', 'lah', 'kah', 'nya']
    
    # Step 2: Coba hilangkan suffix dulu
    temp_word = word
    for s in suffixes:
        if temp_word.endswith(s):
            temp_word = temp_word[:-len(s)]
            removed_suffix = s
            process_steps.append(f"• Menghapus suffix '-{s}': '{word}' → '{temp_word}'")
            break
    
    # Step 3: Cek hasil setelah hilangkan suffix
    if temp_word in KAMUS:
        process_steps.append(f"✓ Hasil '{temp_word}' ditemukan di kamus")
        return {
            'original': original_word,
            'result': temp_word,
            'prefix_removed': None,
            'suffix_removed': removed_suffix,
            'in_dictionary': True,
            'steps': process_steps
        }
    
    # Step 4: Coba hilangkan prefix
    for p in prefixes:
        if temp_word.startswith(p):
            result = temp_word[len(p):]
            removed_prefix = p
            process_steps.append(f"• Menghapus prefix '{p}-': '{temp_word}' → '{result}'")
            
            if result in KAMUS:
                process_steps.append(f"✓ Hasil '{result}' ditemukan di kamus")
                return {
                    'original': original_word,
                    'result': result,
                    'prefix_removed': removed_prefix,
                    'suffix_removed': removed_suffix,
                    'in_dictionary': True,
                    'steps': process_steps
                }
            
            if len(result) > 2:
                process_steps.append(f"• Hasil '{result}' tidak di kamus tapi valid (>2 karakter)")
                return {
                    'original': original_word,
                    'result': result,
                    'prefix_removed': removed_prefix,
                    'suffix_removed': removed_suffix,
                    'in_dictionary': False,
                    'steps': process_steps
                }
    
    # Step 5: Coba urutan terbalik (prefix dulu)
    temp_word = word
    for p in prefixes:
        if temp_word.startswith(p):
            temp_word = temp_word[len(p):]
            if removed_prefix is None:
                removed_prefix = p
                process_steps.append(f"• Mencoba hapus prefix '{p}-': '{word}' → '{temp_word}'")
            break
    
    if temp_word in KAMUS:
        process_steps.append(f"✓ Hasil '{temp_word}' ditemukan di kamus")
        return {
            'original': original_word,
            'result': temp_word,
            'prefix_removed': removed_prefix,
            'suffix_removed': None,
            'in_dictionary': True,
            'steps': process_steps
        }
    
    # Step 6: Hilangkan suffix dari hasil prefix
    for s in suffixes:
        if temp_word.endswith(s):
            result = temp_word[:-len(s)]
            if removed_suffix is None:
                removed_suffix = s
                process_steps.append(f"• Menghapus suffix '-{s}': '{temp_word}' → '{result}'")
            
            if result in KAMUS:
                process_steps.append(f"✓ Hasil '{result}' ditemukan di kamus")
                return {
                    'original': original_word,
                    'result': result,
                    'prefix_removed': removed_prefix,
                    'suffix_removed': removed_suffix,
                    'in_dictionary': True,
                    'steps': process_steps
                }
            
            if len(result) > 2:
                process_steps.append(f"• Hasil '{result}' tidak di kamus tapi valid (>2 karakter)")
                return {
                    'original': original_word,
                    'result': result,
                    'prefix_removed': removed_prefix,
                    'suffix_removed': removed_suffix,
                    'in_dictionary': False,
                    'steps': process_steps
                }
    
    # Final: Return hasil terbaik
    if len(temp_word) >= 3:
        process_steps.append(f"• Menggunakan hasil '{temp_word}' (>= 3 karakter)")
        return {
            'original': original_word,
            'result': temp_word,
            'prefix_removed': removed_prefix,
            'suffix_removed': removed_suffix,
            'in_dictionary': False,
            'steps': process_steps
        }
    else:
        process_steps.append(f"⚠ Tidak dapat di-stem, menggunakan kata asli '{word}'")
        return {
            'original': original_word,
            'result': word,
            'prefix_removed': None,
            'suffix_removed': None,
            'in_dictionary': False,
            'steps': process_steps
        }

def stemming_process(tokens):
    return [stemming_ays(t) for t in tokens]
