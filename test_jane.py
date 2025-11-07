import pytest, hashlib
from jane import crack_passwords
#Use default wordlist.txt and hashes.txt for testing

#Test password cracking functionality
def test_crack_passwords_md5():
    cracked = crack_passwords('hashes.txt', 'wordlist.txt','md5')
    for hsh, pwd in cracked.items():
        assert hashlib.md5(pwd.encode()).hexdigest() == hsh

def test_crack_passwords_sha1():
    cracked = crack_passwords('hashes.txt', 'wordlist.txt','sha1')
    for hsh, pwd in cracked.items():
        assert hashlib.sha1(pwd.encode()).hexdigest() == hsh

def test_crack_passwords_sha256():
    cracked = crack_passwords('hashes.txt', 'wordlist.txt','sha256')
    for hsh, pwd in cracked.items():
        assert hashlib.sha256(pwd.encode()).hexdigest() == hsh


#Test Edge cases
def test_crack_passwords_invalid_file():
    cracked = crack_passwords('nonexistent_hashes.txt', 'nonexistent_wordlist.txt','md5')
    assert cracked == {}

def test_crack_passwords_unsupported_algorithm():
    cracked = crack_passwords('hashes.txt', 'wordlist.txt','unsupported_algo')
    assert cracked == {}

def test_crack_passwords_empty_files():
    cracked = crack_passwords('', '','')
    assert cracked == {}

if __name__ == '__main__':
    pytest.main()