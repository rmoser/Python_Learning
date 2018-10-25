function vf=calcf(str,num)
vf = java.util.Hashtable;
i = 1; nn = size(str);
while i<=nn(2)
    wrd = str(i:i+num-1); i = i+num; addwf(wrd,vf,1);
end

function addwf(word,hash,fr)
wf = hash.get(word);
if size(wf)==0 hash.put(word,fr); else hash.put(word,fr+wf); end

function fr=getwf(word,hash)
wf = hash.get(word);
if size(wf)==0 fr=0; else fr=wf; end