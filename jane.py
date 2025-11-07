#Jane the Ripper - A simple password cracker using multithreading

#Imports
algorithm=''
hash_file_path=''
wordlist_path=''
import hashlib
import threading
def ux():
    global algorithm, hash_file_path, wordlist_path

    #Load our wordlist into memory
    hash_file_path = input("Enter the path to the hash file: ")
    if not hash_file_path:
        hash_file_path= 'hashes.txt'
    wordlist_path = input("Enter the path to the wordlist file: ")
    if not wordlist_path:
        wordlist_path= 'wordlist.txt'

    algorithm = input("Enter the hashing algorithm (md5/sha1/sha256): ").lower()
    if algorithm not in ['md5', 'sha1', 'sha256']:
        print("Unsupported algorithm. Defaulting to md5.")
        algorithm = 'md5'

#Main cracking function
def crack_passwords(hash_file_path, wordlist_path,algorithm):
    if algorithm not in ['md5', 'sha1', 'sha256']:
        print(f"Unsupported algorithm: {algorithm}")
        return {}
    #Load our hashes into memory
    try:
        with open(hash_file_path, 'r') as hash_file:
            hashes = {line.strip() for line in hash_file}
    except FileNotFoundError:
        print(f"Hash file not found: {hash_file_path}")
        return {}
    #Load our wordlist into memory
    try:
        with open(wordlist_path, 'r') as wordlist_file:
            wordlist = [line.strip() for line in wordlist_file]
    except FileNotFoundError:
        print(f"Wordlist file not found: {wordlist_path}")
        return {}
    cracked_passwords = {}
    #Setup true multithreading
    def worker(word_subset):
        #Handles and iterates through a subset of the wordlist
        for word in word_subset:
            if algorithm == 'sha1':
                hashed_word = hashlib.sha1(word.encode()).hexdigest()
            elif algorithm == 'sha256':
                hashed_word = hashlib.sha256(word.encode()).hexdigest()
            else:
                hashed_word = hashlib.md5(word.encode()).hexdigest()
            if hashed_word in hashes:
                #Store cracked password
                cracked_passwords[hashed_word] = word
    num_threads = 4
    #Define our storage
    threads = []
    subset_size = len(wordlist) // num_threads
    for i in range(num_threads):
        start_index = i * subset_size
        end_index = (i + 1) * subset_size if i != num_threads - 1 else len(wordlist)
        thread = threading.Thread(target=worker, args=(wordlist[start_index:end_index],))
        threads.append(thread)
        #Start the thread
        thread.start()
    for thread in threads:
        thread.join()
        #Wait for all threads to finish
    return cracked_passwords

if __name__ == '__main__':
    ux()
    cracked = crack_passwords(hash_file_path, wordlist_path,algorithm)
    for hsh, pwd in cracked.items():
        print(f'Cracked: {hsh} -> {pwd}')