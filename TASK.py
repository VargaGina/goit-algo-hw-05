#TASCK 1
class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(size)]

    def hash_function(self, key):
        return hash(key) % self.size

    def insert(self, key, value):
        index = self.hash_function(key)

        for item in self.table(index):
            if item[0] == key:
                item[1] = value
                return
        self.table[index].append([key, value])

    def search(self, key):
        index = self.hash_function(key)
        for item in self.table[index]:
            if item[0] == key:
                return item[1]
        return None

    def delete(self, key):
        index = self.hash_function(key)
        for i, item in enumerate(self.table[index]):
            if item[0] == key:
                del self.table[index][i]
                return 
        

# Example Usage
ht = HashTable(10)
ht.insert("apple", "10")
print(ht.search("apple"))  
ht.delete("apple")
print(ht.search("apple")) 


#TASCK 2

def binary_search(arr, target):
    left, right = 0 ,len(arr) - 1
 

    while left <= right:
        mid = left + (right - left) // 2

        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

#TASCK 3

def bad_character_rule( pattern):
    m = len(pattern)
    bad_char_table = {}
    
    
    for i in range(m):
        bad_char_table[pattern[i]] = i
    
    return bad_char_table
def is_prefix(pattern, p):
    m = len(pattern)
    j = 0
    for i in range(p, m):
        if pattern[i] != pattern[j]:
            return False
        j += 1
    return True

def suffix_length(pattern, p):
    length = 0
    i = p
    j = len(pattern) - 1
    while i >= 0 and pattern[i] == pattern[j]:
        length += 1
        i -= 1
        j -= 1
    return length

def good_suffix_rule( pattern):
    m = len(pattern)
    good_suffix_table= [0] * m
    border_table=[0]*m
    
    last_prefix_position=m
    
    for i in range(m-1, -1,-1):
        if is_prefix(pattern, i+1):
            last_prefix_position=i+1
        good_suffix_table[i]=last_prefix_position-i+m-1

    for i in range(m-1):
        lenght=suffix_length(pattern, i)
        border_table[lenght]=i

    for i in range(m-1):
        if good_suffix_table[i]==0:
            good_suffix_table[i]= border_table[i]

    return good_suffix_table

def boyer_moore(text, pattern):
    m = len(pattern)
    n = len(text)
    
    bad_char_table=bad_character_rule(pattern)
    good_suffix_table=good_suffix_rule(pattern)
    
    
    s = 0
    while s <= n - m:
        j = m - 1
        
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1
        
        if j < 0:
            return s
        else:
            bad_char_shift = j - bad_char_table.get(text[s + j], -1)
            good_suffix_shift = good_suffix_table[j] if j < m - 1 else 1
            
            s += max(bad_char_shift, good_suffix_shift)

    return -1


def compute_prefix_function( pattern):
    M = len(pattern)
    pi=[0]*M
    k=0
    
    for i in range(1, M):
        while k>0 and pattern[k] != pattern[i]:
            k=pi[k-1]

        if pattern[k]==pattern[i]:
            k+=1

        pi[i]=k

    return pi

def kmp_search(text, pattern):
    M= len(pattern)
    N = len(text)
    pi=compute_prefix_function(pattern)
    j = 0
    
    
    for i in range(N):
        while j>0 and pattern[j] != text[i]:
            j=pi[j-1]

        if pattern[j]==text[i]:
            j+=1

        if j == M:
            return i - M + 1

    return -1

def rabin_karp(text, pattern, base=256, prime=101):
    M = len(pattern)
    N= len(text)
    
    if M>N:
        return -1
    
    pattern_hash=0
    text_hash=0
    h=1
    
    for i in range(M - 1):
        h = (h * base) % prime
    
    for i in range(M):
        pattern_hash=(base*pattern_hash+ord(pattern[i]))%prime
        text_hash=(base*text_hash+ord(text[i]))%prime

    
    for i in range(N - M + 1):
        if pattern_hash == text_hash:
                if text[i:i + M] == pattern:
                    return i
        
        if i < N - M:
            text_hash = (base * (text_hash - ord(text[i]) * h) + ord(text[i + M])) % prime
            if text_hash < 0:
                text_hash += prime
    
    return -1



#Measure
import timeit

# Load articles
with open('/content/article1.txt', 'r') as file:
    text1 = file.read()

with open('/content/article2.txt', 'r') as file:
    text2 = file.read()

# Substrings for testing
substring_exists = "sorting"
substring_not_exists = "nonexistentword"

# Measure execution times
def measure_execution_time(algorithm, text, pattern):
    time=timeit.Timer(lambda:algorithm(text, pattern))
   
    return timeit.timeit(number=1)

algorithms = {"Boyer-Moore":boyer_moore,
              "Knuth-Morris-Pratt":kmp_search,
               "Rabin-Karp": rabin_karp}

texts= {"article1":text1,
       "article2":text2}

patterns= {"existing": substring_exists,
           "madeup":substring_not_exists}

results={}

for algo_name, algorithm in algorithms.items():
    results[algo_name]={}
    for text_name, text in texts.items():
        results[algo_name][text_name]={}
        for pattern_name, pattern in patterns.items():
            time_taken=measure_execution_time(algorithm, text, pattern)
            results[algo_name][text_name][pattern_name]=time_taken



for algo_name, algo_results in results.items():
    print(f"{algo_name}:")
    for text_name, text_results in algo_results.items():
        print(f"{text_name}:")
        for pattern_name, time_taken in text_results.items():
            print(f" {pattern_name}: {time_taken:.6f} seconds")
        