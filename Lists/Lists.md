# List Status

| List         | Original | All / Post-Strip | Passed | Dead | Date       | Commit  |
|--------------|---------:|-----------------:|-------:|-----:|-----------:|--------:|
| Custom       |          | 10365            | 7763   | 2602 | May 7 2018 |         |
| UT1          | 1938667  | 617956           | 
| Sinfonietta  | 7054     | 7047             | 4283   | 2765 | May 7 2018 | 1904ea3 |
| Clefspeare13 | 6088     | 5287             | 2859   | 2429 | May 7 2017 | d9b61ae |

### Folder Breakdown:
> custom:
>> results: (Results from domain testing)
>> sources: (Original Sources)

> UT1:
>> results: (Results from domain testing)

> Sinfonietta:
>> sources: (Original files)  
>> results: (Results from domain testing)

> Clefspeare13:
>> sources: (Original files)  
>> results: (Results from domain testing)

# Sources for all the lists used

### custom_list:
1. [reddit: jacop_](https://www.reddit.com/u/jacop_)

   source: [/r/NoFap](https://redd.it/3l89jz)
   
   changes:
     1. Removed all '/' at end of domains
     2. Removed duplicates
     3. Reformatted from hosts format
     4. Also added www subdomain for websites
     
2. [reddit: th0mm_](https://www.reddit.com/u/th0mm_)
   
    source: [/r/NoFap](https://redd.it/6cplet)
    
    changes: 
      1. Removed duplicates
      2. Reformatted from hosts format
      3. Also added www subdomain for websites
      
3. Custom:

   source: Domains collected from Google
   

## Edited Custom Lists:

### UT1 Blacklist:

source: [Université Toulouse 1 Capitole](https://dsi.ut-capitole.fr/blacklists/index_en.php)

changes: 
  1. Remove all IP addresses since they cannot be blocked by pi-hole
  2. Remove all blacklisted domains (mainly tumblr and blogspot)
  3. Add www subdomains for all websites
  3. Remove all websites that are dead
     1. Do not resolve
     2. Do not return a HTTP response code under 400

### Sinfonietta:

source: [Github](https://github.com/Sinfonietta/hostfiles)

changes:
  1. Reformatted from hosts format
  2. Remove all blacklisted domains (mainly tumblr and blogspot)
  3. Remove all websites that are dead
     1. Do not resolve
     2. Do not return a HTTP response code under 400
     
### Clefspeare13:

source: [Github](https://github.com/Clefspeare13/pornhosts)

changes:
  1. Reformatted from hosts format
  2. Remove all blacklisted domains (mainly tumblr and blogspot)
  3. Remove all websites that are dead
     1. Do not resolve
     2. Do not return a HTTP response code under 400

## Public Lists:


# Maintaining the Lists
### Process for Updating (Once/ Month)
1. Download new File
   1. Check if hashes differ
2. Apply same stripping and purging
3. awk using all to find new sites
   1. Run sites through checker
4. Recheck pass sites from last run
5. Test new sites

### Process for Validation
1. Find sites in all but not in pass or dead
   1. Run sites through checker
2. Re-run dead with 30 concurrent threads
3. Re-run pass 


