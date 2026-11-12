Action()
{

	web_url("DigiCertEVRSACAG2.crt", 
		"URL=http://cacerts.digicert.com/DigiCertEVRSACAG2.crt", 
		"Resource=1", 
		"RecContentType=application/pkix-cert", 
		"Referer=", 
		"Snapshot=t14.inf", 
		LAST);

	web_url("generate_204", 
		"URL=http://edge-http.microsoft.com/captiveportal/generate_204", 
		"Resource=0", 
		"Referer=", 
		"Snapshot=t15.inf", 
		"Mode=HTML", 
		EXTRARES, 
		"Url=http://cacerts.digicert.com/DigiCertEVRSACAG2.crt", "Referer=", ENDITEM, 
		LAST);

	web_set_sockets_option("SSL_VERSION", "AUTO");

	web_url("blocklist", 
		"URL=https://edge.microsoft.com/abusiveadblocking/api/v1/blocklist", 
		"Resource=0", 
		"RecContentType=application/json", 
		"Referer=", 
		"Snapshot=t16.inf", 
		"Mode=HTML", 
		LAST);

	web_add_cookie("MSCC=cid=hpbga8026xhkis0s9bdj82k8-c1=2-c2=2-c3=2; DOMAIN=edge.microsoft.com");

	web_add_cookie("MC1=GUID=081da2f87ecc439484704654ba8ff8bc&HASH=081d&LV=202604&V=4&LU=1776296329867; DOMAIN=edge.microsoft.com");

	web_custom_request("msa", 
		"URL=https://edge.microsoft.com/identity/api/v3/msa", 
		"Method=POST", 
		"Resource=0", 
		"RecContentType=application/json", 
		"Referer=", 
		"Snapshot=t17.inf", 
		"Mode=HTML", 
		"EncType=application/json", 
		"Body={\"disable_features\":\"350d8d88,6231a2c,a7ebb679,84a7a725,f40dd80c,9016c43c,f77be41b,c883a9e1,d20037d8,fbbe90c8,84e76b2b,e6cb651f,9b42372\",\"enable_features\":\"982d40a7,5937c249,c532719a,422c613a,61da859c,36e08b64,94fd730b,4dba0481,97f2a1,49bb88f2,8beffa8c,679d1a6b,5920a7a,96986692,53151ee7,e8381174,ca3e150a,5c04a507,67ed34ba,ddfd6cd3,d8475dc5,f93d1392,e28e66a,fa02242b,27e96171,f22e8def,82ba5025,87b33764,59b2acdd,9df1b21b,75b1b341,5649efc3,e5dfa3e1,3b060bb,f6e73e9,1009bf4a,1207cc22,"
		"3891021f,2373949a,55a5f854,21714a50,9e8c649c,1cb7bd90,fbee8c48,723e8d09,6ed7bcf6,100a933e,83d96976,7c518418,e28a1926,f8f430d4,d2279a12,c44ef1ed,ace2c02,62fd93b7,f44e49cb,67dd119c,866d5317,1c10837e,2fe969f,c1a41ff,951654f3,de6be500,d3dcbbe5,902b12ef,bab9ed83,4da78b64,e02966fa,86b5a241,e57a4904,1ccbc1c,b05c236d,126803bb,8f5ff88b,8cc8dcf4,766eb917,b905a3b3,33caa06a,3bb18b6a,3061cce0,75b4dbd6,57df5455,52006c6,e6245753,ea1da90a,48885bc6,25485ab7,e3ce9af1,8c6c76e5,78fcf7c1,a606eeb4\",\"filter\":{\""
		"version\":\"150.0.4078.48\"}}", 
		LAST);

	web_custom_request("json", 
		"URL=https://update.googleapis.com/service/update2/json?cup2key=16:CmaFctn04bDx0O2153kQhtrKML-U1oouVeeY2H64ToI&cup2hreq=59d7a2ab1019258ce90043fd8ed43080c948668da209ad77f13f2f4fb49d6be5", 
		"Method=POST", 
		"Resource=0", 
		"RecContentType=application/json", 
		"Referer=", 
		"Snapshot=t18.inf", 
		"Mode=HTML", 
		"EncType=application/json", 
		"Body={\"request\":{\"@os\":\"win\",\"@updater\":\"chromiumcrx\",\"acceptformat\":\"crx3,download,run,xz,zucc\",\"apps\":[{\"appid\":\"jlhmfgmfgeifomenelglieieghnjghma\",\"cohort\":\"1::\",\"enabled\":true,\"installdate\":6982,\"installedby\":\"internal\",\"lang\":\"en-US\",\"ping\":{\"ping_freshness\":\"{63b4ab0d-09bd-4fe7-b177-6adffb83d7aa}\",\"rd\":7125},\"targetingattributes\":{\"AppCohort\":\"1::\",\"AppMajorVersion\":\"150\",\"AppRollout\":0,\"AppVersion\":\"150.0.4078.48\",\"IsInternalUser\""
		":false,\"Priority\":false},\"updatecheck\":{},\"version\":\"2.0.4\"},{\"appid\":\"ljdobmomdgdljniojadhoplhkpialdid\",\"cohort\":\"1::\",\"enabled\":true,\"installdate\":6982,\"installedby\":\"internal\",\"lang\":\"en-US\",\"ping\":{\"ping_freshness\":\"{61d57c3c-bef6-4acf-9741-27d1770d6116}\",\"rd\":7125},\"targetingattributes\":{\"AppCohort\":\"1::\",\"AppMajorVersion\":\"150\",\"AppRollout\":0,\"AppVersion\":\"150.0.4078.48\",\"IsInternalUser\":false,\"Priority\":false},\"updatecheck\":{},\""
		"version\":\"7.1.0\"},{\"appid\":\"mbopgmdnpcbohhpnfglgohlbhfongabi\",\"cohort\":\"1::\",\"enabled\":true,\"installdate\":6982,\"installedby\":\"internal\",\"lang\":\"en-US\",\"ping\":{\"ping_freshness\":\"{9ffd5880-086f-46f7-9a7a-38412563cf1c}\",\"rd\":7125},\"targetingattributes\":{\"AppCohort\":\"1::\",\"AppMajorVersion\":\"150\",\"AppRollout\":0,\"AppVersion\":\"150.0.4078.48\",\"IsInternalUser\":false,\"Priority\":false},\"updatecheck\":{},\"version\":\"6.6.10\"}],\"arch\":\"x64\",\"dedup\":\""
		"cr\",\"domainjoined\":false,\"hw\":{\"avx\":1,\"physmemory\":31,\"sse\":1,\"sse2\":1,\"sse3\":1,\"sse41\":1,\"sse42\":1,\"ssse3\":1},\"ismachine\":1,\"os\":{\"arch\":\"x86_64\",\"platform\":\"Windows\",\"version\":\"10.0.26200.8655\"},\"prodversion\":\"150.0.4078.48\",\"protocol\":\"4.0\",\"requestid\":\"{82d7dee5-5343-44a6-b766-7788432a55b1}\",\"sessionid\":\"{cc452922-a7c1-424f-8d9a-16402ae199f2}\",\"updaterversion\":\"150.0.4078.48\"}}", 
		LAST);

	web_custom_request("update", 
		"URL=https://edge.microsoft.com/componentupdater/api/v1/update?cup2key=7:X8ZDtV2kVi55tMJ1qEE6h2GWMq9L2WGsP0UH2Yu7V8w&cup2hreq=d8a5a6db4991c3d8d29b18c3b311bba98b8340dc90a47bc1463552d4ad5c1f5e", 
		"Method=POST", 
		"Resource=0", 
		"RecContentType=application/json", 
		"Referer=", 
		"Snapshot=t19.inf", 
		"Mode=HTML", 
		"EncType=application/json", 
		"Body={\"request\":{\"@os\":\"win\",\"@updater\":\"msedge\",\"acceptformat\":\"crx3,download,run,xz,zucc\",\"apps\":[{\"appid\":\"nmcnjaceoejcjmmnabjnmfpoanaengif\",\"brand\":\"EPBR\",\"cached_items\":[{\"sha256\":\"a9592ae40712c6cfdf7d142e2563ca4ec8f696cfe53e267ad0ea630c43beaa33\"}],\"cohort\":\"rrf@0.10\",\"enabled\":true,\"installdate\":-1,\"lang\":\"en-US\",\"ping\":{\"r\":-2},\"targetingattributes\":{\"AppCohort\":\"rrf@0.10\",\"AppMajorVersion\":\"150\",\"AppRollout\":0.1,\"AppVersion\":\""
		"150.0.4078.48\",\"IsInternalUser\":false,\"Priority\":false,\"Updater\":\"Omaha\",\"UpdaterVersion\":\"1.3.241.15\"},\"updatecheck\":{},\"version\":\"2026.1.30.1\"}],\"arch\":\"x64\",\"dedup\":\"cr\",\"domainjoined\":false,\"hw\":{\"avx\":1,\"physmemory\":31,\"sse\":1,\"sse2\":1,\"sse3\":1,\"sse41\":1,\"sse42\":1,\"ssse3\":1},\"ismachine\":1,\"os\":{\"arch\":\"x86_64\",\"platform\":\"Windows\",\"version\":\"10.0.26200.8655\"},\"prodversion\":\"150.0.4078.48\",\"protocol\":\"4.0\",\"requestid\":\""
		"{86b63da1-3424-4b24-ad2e-aa7c00182d7c}\",\"sessionid\":\"{9931dada-3fe3-4805-8857-d8dc9ab6e11d}\",\"updaters\":{\"autoupdatecheckenabled\":true,\"ismachine\":1,\"lastchecked\":0,\"laststarted\":0,\"name\":\"Omaha\",\"updatepolicy\":-1,\"version\":\"1.3.241.15\"},\"updaterversion\":\"150.0.4078.48\"}}", 
		LAST);

	web_add_cookie("ANON=; DOMAIN=www.bing.com");

	web_add_cookie("MUID=322652E64203617C029B441943C66007; DOMAIN=www.bing.com");

	web_add_cookie("_RwBf=r=1F9038E3727D83B63,AC0F09C0F8BF5E7A&mta=0&ispd=0&rc=278&rb=278&rg=0&pc=278&mtu=0&rbb=0.0&clo=0&v=1&l=2026-06-28T07:00:00.0000000Z&lft=0001-01-01T00:00:00.0000000&aof=0&ard=0001-01-01T00:00:00.0000000&rwdbt=1758426301&rwflt=1691479545&rwaul2=0&g=newLevel1&o=0&p=bingcopilotwaitlist&c=ML2DSE&t=6850&s=2023-03-20T19:55:03.6423467+00:00&ts=2026-06-28T21:31:48.7712743+00:00&rwred=0&wls=2&wlb=0&wle=0&ccp=2&cpt=0&lka=0&lkt=0&aad=0&TH=&cid=3&gb=2025w27_c&e="
		"e_gpPf3E4LVkEc_4-ZKJ-9_46PbvE-w2kFE8n8ArH_st3HNwj-2Dx3meMy87w3gCaGqu-22Phj8zUqV4T-Q0Ng&A=; DOMAIN=www.bing.com");

	web_url("shoppingsettings", 
		"URL=https://www.bing.com/api/shopping/v1/user/shoppingsettings", 
		"Resource=0", 
		"RecContentType=application/json", 
		"Referer=", 
		"Snapshot=t20.inf", 
		"Mode=HTML", 
		LAST);

	web_custom_request("crx", 
		"URL=https://edge.microsoft.com/extensionwebstorebase/v1/crx", 
		"Method=POST", 
		"Resource=0", 
		"RecContentType=application/json", 
		"Referer=", 
		"Snapshot=t21.inf", 
		"Mode=HTML", 
		"EncType=application/json", 
		"Body={\"request\":{\"@os\":\"win\",\"@updater\":\"msedgecrx\",\"acceptformat\":\"crx3,download,run,xz,zucc\",\"apps\":[{\"appid\":\"ajdpfmkffanmkhejnopjppegokpogffp\",\"cohort\":\"rrf@0.70\",\"enabled\":true,\"installdate\":6983,\"installedby\":\"internal\",\"lang\":\"en-US\",\"ping\":{\"ping_freshness\":\"{b68d16c0-2d55-4f66-8a26-4104dcc76fb2}\",\"rd\":7125},\"targetingattributes\":{\"AppCohort\":\"rrf@0.70\",\"AppMajorVersion\":\"150\",\"AppRollout\":0.7,\"AppVersion\":\"150.0.4078.48\",\""
		"IsInternalUser\":false,\"Priority\":false},\"updatecheck\":{},\"version\":\"3.17.0\"},{\"appid\":\"jmjflgjpcpepeafmmgdpfkogkghcpiha\",\"cohort\":\"rrf@0.09\",\"enabled\":true,\"installdate\":6983,\"installedby\":\"other\",\"lang\":\"en-US\",\"ping\":{\"ping_freshness\":\"{904b899c-1874-42b2-a046-798abc1dc8e6}\",\"rd\":7125},\"targetingattributes\":{\"AppCohort\":\"rrf@0.09\",\"AppMajorVersion\":\"150\",\"AppRollout\":0.09,\"AppVersion\":\"150.0.4078.48\",\"IsInternalUser\":false,\"Priority\":false"
		"},\"updatecheck\":{},\"version\":\"1.2.1\"},{\"appid\":\"mmdeekfbniconmppklfobaikbmdanboc\",\"cohort\":\"rrf@0.73\",\"enabled\":true,\"installdate\":6983,\"installedby\":\"internal\",\"lang\":\"en-US\",\"ping\":{\"ping_freshness\":\"{4c73711f-44eb-4b1b-94f1-2380c1e6a72b}\",\"rd\":7125},\"targetingattributes\":{\"AppCohort\":\"rrf@0.73\",\"AppMajorVersion\":\"150\",\"AppRollout\":0.73,\"AppVersion\":\"150.0.4078.48\",\"IsInternalUser\":false,\"Priority\":false},\"updatecheck\":{},\"version\":\""
		"1.0.1\"}],\"arch\":\"x64\",\"dedup\":\"cr\",\"domainjoined\":false,\"hw\":{\"avx\":1,\"physmemory\":31,\"sse\":1,\"sse2\":1,\"sse3\":1,\"sse41\":1,\"sse42\":1,\"ssse3\":1},\"ismachine\":1,\"os\":{\"arch\":\"x86_64\",\"platform\":\"Windows\",\"version\":\"10.0.26200.8655\"},\"prodversion\":\"150.0.4078.48\",\"protocol\":\"4.0\",\"requestid\":\"{638405d5-ec8d-431a-8257-a8524da0fb79}\",\"revocationviaomahaenabled\":\"1\",\"sessionid\":\"{87136450-768e-411e-9b2c-9f92df2f9a31}\",\"updaterversion\":\""
		"150.0.4078.48\"}}", 
		LAST);

	/*Possible OAUTH authorization was detected. It is recommended to correlate the authorization parameters.*/

	web_add_cookie("_EDGE_V=1; DOMAIN=www.bing.com");

	web_add_cookie("SRCHD=AF=NOFORM; DOMAIN=www.bing.com");

	web_add_cookie("SRCHUID=V=2&GUID=E473FD3DE36044DD9D5DE7C56355E191&dmnchg=1; DOMAIN=www.bing.com");

	web_add_cookie("ANON=A=35C76470417CB88CDB53D001FFFFFFFF; DOMAIN=www.bing.com");

	web_add_cookie("SRCHUSR=DOB=20260213&DS=1; DOMAIN=www.bing.com");

	web_add_cookie("MSCCSC=1; DOMAIN=www.bing.com");

	web_add_cookie("MMCASM=ID=9CAE46BA409C44FF8B5F60C41F5964FA; DOMAIN=www.bing.com");

	web_add_cookie("_C_Auth=; DOMAIN=www.bing.com");

	web_add_cookie("CortanaAppUID=9264347B3FFD899D58E69194CC6EE99B; DOMAIN=www.bing.com");

	web_add_cookie("_EDGE_S=F=1&SID=07FADAD19A6760B13587CC2E9BA261F8&mkt=en-ca&ui=en-ca; DOMAIN=www.bing.com");

	web_add_cookie("_uetvid=975215f018c011f193d54322ac4f685f; DOMAIN=www.bing.com");

	web_add_cookie("_uetmsclkid=_uete1ec00b001061fe751d6696cdb18353c; DOMAIN=www.bing.com");

	web_add_cookie("_SS=SID=07FADAD19A6760B13587CC2E9BA261F8&PC=LCTS&R=278&RB=278&GB=0&RG=0&RP=278&OCID=M4067T; DOMAIN=www.bing.com");

	web_add_cookie("USRLOC=HS=1&ELOC=LAT=43.603843688964844|LON=-79.5445327758789|N=Toronto%2C%20Ontario|ELT=2|&CLOC=LAT=43.607092765796615|LON=-79.55562735961496|A=733.4464586120832|TS=260628213148|SRC=W&BID=MjYwNjI4MTczMTQ4Xzg3YmViM2U5Zjc5NWQ4YzJlMWMzZGE1NTk1MTY3OWEzY2RjMjEyOGY1M2NhNTNhZjM0YTYxMzZmMmNhMzI3OWE=; DOMAIN=www.bing.com");

	web_add_cookie("fbar=imgfbar=1; DOMAIN=www.bing.com");

	web_add_cookie("SRCHHPGUSR=SRCHLANG=en&PV=19.0.0&PREFCOL=0&BRW=XW&BRH=M&CW=1912&CH=901&SCW=1897&SCH=2213&DPR=1.0&UTC=-240&B=0&EXLTT=12&HV=1782682308&HVE=CfDJ8A8rLfEh4ZdMhJ19YNJ4FtSTxX8Ub40gix5Ecvgc2HN8LNPpKxbm3TxaSCR9_ro_7pIKjzUa9h7KfXmM5qq5pSYwaCijsfoqv-F_4krQEtYCamr17NhsP8W4XR8PHqnGH6NUqy-hoomZu0DzatKHjv0dVkJasX8KfAWmQSp1P30J&PRVCW=1912&PRVCH=948&AV=14&ADV=14&RB=0&MB=0; DOMAIN=www.bing.com");

	web_add_cookie("_C_ETH=1; DOMAIN=www.bing.com");

	web_add_cookie("_Rwho=u=d&ts=2026-06-28; DOMAIN=www.bing.com");

	web_add_cookie("_clck=u5nio9%5E2%5Eg7a%5E0%5E2370; DOMAIN=www.bing.com");

	web_add_cookie("WLS=C=00000000-0000-0000-dfb8-ff1bd982f098&N=Weipeng+Zheng; DOMAIN=www.bing.com");

	web_add_cookie(".MSA.Auth=CfDJ8A8rLfEh4ZdMhJ19YNJ4FtQBe1Sq0E-FpJrEpYt70xikLcpiIbsCeoCCD4dtXNyl4RzmE9emBoztv6g4nIuiQh7mit6m2-clkxp9KyrTFpUvbgQiX3t88RWQjTLMOF6K7-g25k9qUW1Y4V62edbgN2guckFt93dbnZ3RxRjYYDGUC0GESHPrNJCeBuRmq5Y_XpHMM65AWF-8QGNqQ2GQMXjfT8XHgG8QgmZjAQHL0m1Zu3owbBQWDLYLbrOjooYANQPBd6HCfK8QfwthoE3gaOokdOSylFMAqWS4LbXn6n1Pqw0S1ctn-huKBNvrLeKqXp1KMrGPJ5ouA-OhTTbWhd8Vb_jiNRoY9fRbBQ5JgVtPO8aK0wPkn4uMNkrmWKgMm5xKDQVXUj6dxO4PTdGtBJICvtUHe8wVlF2CVTR9ksQ6; DOMAIN=www.bing.com");

	web_add_cookie("_U=1t15kFzNhIpBG2gIw3gj7S4lcv6xyfoDkYp1yUzygGBykwGOvKd0lHrRUtfSPJvVl_oLzAjFbZHL4CZwbFmq7AW99dB6_KIBtXUgY1wBKk48EQ_4xjgLkzjP65UpVZIB66SAQ089pU8JKyiKRiFKt2d_tnYDIIUeNvvPeo28rUAmqn2qrlr5_gOksEicsRUo8ZY0W2XtUYwFttvC0J594NQIgWItT9ZExyk82AZ2r_zg; DOMAIN=www.bing.com");

	web_url("v2", 
		"URL=https://www.bing.com/fd/auth/signin/v2?action=header", 
		"Resource=0", 
		"RecContentType=text/html", 
		"Referer=", 
		"Snapshot=t22.inf", 
		"Mode=HTML", 
		LAST);

	web_url("V1Profile", 
		"URL=https://substrate.office.com/profileb2/v2.0/me/V1Profile", 
		"Resource=0", 
		"RecContentType=application/json", 
		"Referer=", 
		"Snapshot=t23.inf", 
		"Mode=HTML", 
		LAST);

	web_custom_request("command", 
		"URL=https://edge.microsoft.com/sync/v1/feeds/me/syncEntities/command/?client=Chromium&client_id=fG%2BQBAAE43Au5Ym6F%2FeYCg%3D%3D", 
		"Method=POST", 
		"Resource=0", 
		"RecContentType=application/octet-stream", 
		"Referer=", 
		"Snapshot=t24.inf", 
		"ContentEncoding=gzip", 
		"Mode=HTML", 
		"EncType=application/octet-stream", 
		"BodyBinary=\n\\x18fG+QBAAE43Au5Ym6F/eYCg==\\x10c\\x18\\x02*\\xEB\\x04\\x12\\x02\\x10\\x01\\x18\\x012\\x1E\\x08\\x88\\x81\\x02\\x12\\x08\\xECbyT\\x9C\\x01\\x00\\x00*\\x0E\\x10\\x00\\x18\\x01 \\x00(\\x040\\x008\\x00@\\x002\\x1E\\x08\\xC6\\xA6\\x02\\x12\\x08o\\xADb4\\x9F\\x01\\x00\\x00*\\x0E\\x10\\x00\\x18\\x01 \\x01(\\x040\\x008\\x00@\\x002\\x1E\\x08\\xB1\\xE6\\x02\\x12\\x08o\\xADb4\\x9F\\x01\\x00\\x00*\\x0E\\x10\\x00\\x18\\x01 \\x00"
		"(\\x040\\x008\\x00@\\x002\\x1E\\x08\\xCF\\xF3\\x03\\x12\\x08o\\xADb4\\x9F\\x01\\x00\\x00*\\x0E\\x10\\x00\\x18\\x01 \\x00(\\x040\\x008\\x00@\\x002\\x1E\\x08\\xF1\\xF7\\x01\\x12\\x08o\\xADb4\\x9F\\x01\\x00\\x00*\\x0E\\x10\\x00\\x18\\x01 \\x00(\\x040\\x008\\x00@\\x002\\x1E\\x08\\xF7\\xF7\\x02\\x12\\x08o\\xADb4\\x9F\\x01\\x00\\x00*\\x0E\\x10\\x00\\x18\\x01 \\x00(\\x040\\x008\\x00@\\x002\\x1E\\x08\\xC7\\x87\\x03\\x12\\x08o\\xADb4\\x9F\\x01\\x00\\x00*\\x0E\\x10\\x00\\x18\\x01 \\x00"
		"(\\x040\\x008\\x00@\\x002\\x1E\\x08\\x9F\\xEF\\x05\\x12\\x08o\\xADb4\\x9F\\x01\\x00\\x00*\\x0E\\x10\\x00\\x18\\x01 \\x00(\\x040\\x008\\x00@\\x002\\x1E\\x08\\xEB\\x95\t\\x12\\x08o\\xADb4\\x9F\\x01\\x00\\x00*\\x0E\\x10\\x00\\x18\\x01 \\x00(\\x040\\x008\\x00@\\x002\\x1E\\x08\\x9A\\xB7\t\\x12\\x08o\\xADb4\\x9F\\x01\\x00\\x00*\\x0E\\x10\\x00\\x18\\x01 \\x02(\\x040\\x008\\x00@\\x002\\x1E\\x08\\xFC\\xDE$\\x12\\x08o\\xADb4\\x9F\\x01\\x00\\x00*\\x0E\\x10\\x00\\x18\\x01 \\x00"
		"(\\x040\\x008\\x00@\\x002\\x1E\\x08\\xC9\\x8B)\\x12\\x08o\\xADb4\\x9F\\x01\\x00\\x00*\\x0E\\x10\\x00\\x18\\x01 \\x00(\\x040\\x008\\x00@\\x002\\x1E\\x08\\x91\\xEB:\\x12\\x08o\\xADb4\\x9F\\x01\\x00\\x00*\\x0E\\x10\\x00\\x18\\x01 \\x00(\\x040\\x008\\x00@\\x002\\x1E\\x08\\xCA\\xAA=\\x12\\x08o\\xADb4\\x9F\\x01\\x00\\x00*\\x0E\\x10\\x00\\x18\\x01 \\x00(\\x040\\x008\\x00@\\x002\\x1E\\x08\\xAB\\xD26\\x12\\x08o\\xADb4\\x9F\\x01\\x00\\x00*\\x0E\\x10\\x00\\x18\\x01 \\x00"
		"(\\x040\\x008\\x00@\\x002\\x1E\\x08\\xD0\\xAF:\\x12\\x08o\\xADb4\\x9F\\x01\\x00\\x00*\\x0E\\x10\\x00\\x18\\x01 \\x00(\\x040\\x008\\x00@\\x002\\x1E\\x08\\xA9\\xF0O\\x12\\x08o\\xADb4\\x9F\\x01\\x00\\x00*\\x0E\\x10\\x00\\x18\\x01 \\x00(\\x040\\x008\\x00@\\x002\\x1E\\x08\\xE4\\x92t\\x12\\x08o\\xADb4\\x9F\\x01\\x00\\x00*\\x0E\\x10\\x00\\x18\\x01 \\x00(\\x040\\x008\\x00@\\x002\\x1E\\x08\\x81\\xF5\\x02\\x12\\x08o\\xADb4\\x9F\\x01\\x00\\x00*\\x0E\\x10\\x00\\x18\\x01 \\x00"
		"(\\x060\\x008\\x00@\\x00H\\x0C\\xC0>\\x01:\\x1FProductionEnvironmentDefinitionR$\n\\x02\\x08\\x05\n\\x02\\x08\t\n\\x02\\x08\n\n\\x04\\x18\\xC6\\xA6\\x02\n\\x04\\x18\\x9A\\xB7\t\n\\x04\\x18\\x9A\\xB7\t\\x10\\x01\\x18\\x00 \\x00Z\\x00b\ndummytokenj\\x02\\x10\\x01r\\x1Cchr:fG+QBAAE43Au5Ym6F/eYCg==", 
		LAST);

	web_url("Profile", 
		"URL=https://substrate.office.com/profileb2/v2.0/me/Profile", 
		"Resource=0", 
		"RecContentType=application/json", 
		"Referer=", 
		"Snapshot=t25.inf", 
		"Mode=HTML", 
		LAST);

	lr_think_time(6);

	web_custom_request("update_2", 
		"URL=https://edge.microsoft.com/componentupdater/api/v1/update?cup2key=7:0nYBLRK3GhUuwq7DeicoeLEhGRq935ND73Z4IKIPYVk&cup2hreq=8fe1add633f24070e4bf5b9cf8326cd3f9ba1db0d81c013c42bfefff9b5ed54a", 
		"Method=POST", 
		"Resource=0", 
		"RecContentType=application/json", 
		"Referer=", 
		"Snapshot=t26.inf", 
		"Mode=HTML", 
		"EncType=application/json", 
		"Body={\"request\":{\"@os\":\"win\",\"@updater\":\"msedge\",\"acceptformat\":\"crx3,download,run,xz,zucc\",\"apps\":[{\"appid\":\"kpfehajjjbbcifeehjgfgnabifknmdad\",\"brand\":\"EPBR\",\"cached_items\":[{\"sha256\":\"00af3f07b5abb71f6d30337e1eef62fa280f06ef19485c0cf6b72171f92ccc0a\"}],\"cohort\":\"rrf@0.77\",\"enabled\":true,\"installdate\":-1,\"lang\":\"en-US\",\"ping\":{\"r\":-2},\"targetingattributes\":{\"AppCohort\":\"rrf@0.77\",\"AppMajorVersion\":\"150\",\"AppRollout\":0.77,\"AppVersion\":\""
		"150.0.4078.48\",\"IsInternalUser\":false,\"Priority\":false,\"Updater\":\"Omaha\",\"UpdaterVersion\":\"1.3.241.15\"},\"updatecheck\":{},\"version\":\"120.0.6050.0\"},{\"appid\":\"oankkpibpaokgecfckkdkgaoafllipag\",\"brand\":\"EPBR\",\"cached_items\":[{\"sha256\":\"fa29a6d5775ff340900a65b39b02fc8b4b77d403c048d8debf22f2f5d09c61a0\"}],\"cohort\":\"rrf@0.87\",\"enabled\":true,\"installdate\":-1,\"lang\":\"en-US\",\"ping\":{\"r\":-2},\"targetingattributes\":{\"AppCohort\":\"rrf@0.87\",\""
		"AppMajorVersion\":\"150\",\"AppRollout\":0.87,\"AppVersion\":\"150.0.4078.48\",\"IsInternalUser\":false,\"Priority\":false,\"Updater\":\"Omaha\",\"UpdaterVersion\":\"1.3.241.15\"},\"updatecheck\":{},\"version\":\"6498.2025.9.4\"},{\"appid\":\"laoigpblnllgcgjnjnllmfolckpjlhki\",\"brand\":\"EPBR\",\"cohort\":\"rrf@0.18\",\"enabled\":true,\"installdate\":-1,\"lang\":\"en-US\",\"ping\":{\"r\":-2},\"targetingattributes\":{\"AppCohort\":\"rrf@0.18\",\"AppMajorVersion\":\"150\",\"AppRollout\":0.18,\""
		"AppVersion\":\"150.0.4078.48\",\"IsInternalUser\":false,\"Priority\":false,\"Updater\":\"Omaha\",\"UpdaterVersion\":\"1.3.241.15\"},\"updatecheck\":{},\"version\":\"1.0.7.1652906823\"},{\"appid\":\"ohckeflnhegojcjlcpbfpciadgikcohk\",\"brand\":\"EPBR\",\"cached_items\":[{\"sha256\":\"95fd9d48e4fc245a3f3a99a3a16ecd1355050ba3f4afc555f19a97c7f9b49677\"}],\"cohort\":\"rrf@0.57\",\"enabled\":true,\"installdate\":-1,\"lang\":\"en-US\",\"ping\":{\"r\":-2},\"targetingattributes\":{\"AppCohort\":\"rrf@0.57"
		"\",\"AppMajorVersion\":\"150\",\"AppRollout\":0.57,\"AppVersion\":\"150.0.4078.48\",\"IsInternalUser\":false,\"Priority\":false,\"Updater\":\"Omaha\",\"UpdaterVersion\":\"1.3.241.15\"},\"updatecheck\":{},\"version\":\"0.0.1.7\"},{\"appid\":\"fgbafbciocncjfbbonhocjaohoknlaco\",\"brand\":\"EPBR\",\"cached_items\":[{\"sha256\":\"a922b7d113e67ce71528805d3c6780f7a207cada8ad56642047577358e46ba3d\"}],\"cohort\":\"rrf@0.43\",\"enabled\":true,\"installdate\":-1,\"lang\":\"en-US\",\"ping\":{\"r\":-2},\""
		"targetingattributes\":{\"AppCohort\":\"rrf@0.43\",\"AppMajorVersion\":\"150\",\"AppRollout\":0.43,\"AppVersion\":\"150.0.4078.48\",\"IsInternalUser\":false,\"Priority\":false,\"Updater\":\"Omaha\",\"UpdaterVersion\":\"1.3.241.15\"},\"updatecheck\":{},\"version\":\"2026.3.23.1\"},{\"appid\":\"ndikpojcjlepofdkaaldkinkjbeeebkl\",\"brand\":\"EPBR\",\"cached_items\":[{\"sha256\":\"720517793663c90e0dbd77cb42709bac49af733f83f73320ba89859d9b0310e0\"}],\"cohort\":\"rrf@0.40\",\"enabled\":true,\""
		"installdate\":-1,\"lang\":\"en-US\",\"ping\":{\"r\":-2},\"targetingattributes\":{\"AppCohort\":\"rrf@0.40\",\"AppMajorVersion\":\"150\",\"AppRollout\":0.4,\"AppVersion\":\"150.0.4078.48\",\"IsInternalUser\":false,\"Priority\":false,\"Updater\":\"Omaha\",\"UpdaterVersion\":\"1.3.241.15\"},\"updatecheck\":{},\"version\":\"10.34.0.84\"},{\"appid\":\"mpicjakjneaggahlnmbojhjpnileolnb\",\"brand\":\"EPBR\",\"cached_items\":[{\"sha256\":\"96b9640eef0668f4d266932438731ee473f9c1186e1c64440512025567be62b7\"}"
		"],\"cohort\":\"rrf@0.13\",\"enabled\":true,\"installdate\":-1,\"lang\":\"en-US\",\"ping\":{\"r\":-2},\"targetingattributes\":{\"AppCohort\":\"rrf@0.13\",\"AppMajorVersion\":\"150\",\"AppRollout\":0.13,\"AppVersion\":\"150.0.4078.48\",\"IsInternalUser\":false,\"Priority\":false,\"Updater\":\"Omaha\",\"UpdaterVersion\":\"1.3.241.15\"},\"updatecheck\":{},\"version\":\"4.0.1.32\"},{\"appid\":\"alpjnmnfbgfkmmpcfpejmmoebdndedno\",\"brand\":\"EPBR\",\"cached_items\":[{\"sha256\":\""
		"bec8ead1da3c9600fe66bbcc0e7a9bed9a184c1be821b4d23570c6b7af7f0410\"}],\"cohort\":\"rrf@0.75\",\"enabled\":true,\"installdate\":-1,\"lang\":\"en-US\",\"ping\":{\"r\":-2},\"targetingattributes\":{\"AppCohort\":\"rrf@0.75\",\"AppMajorVersion\":\"150\",\"AppRollout\":0.75,\"AppVersion\":\"150.0.4078.48\",\"IsInternalUser\":false,\"Priority\":false,\"Updater\":\"Omaha\",\"UpdaterVersion\":\"1.3.241.15\"},\"updatecheck\":{},\"version\":\"46.0.0.0\"},{\"appid\":\"eeobbhfgfagbclfofmgbdfoicabjdbkn\",\""
		"brand\":\"EPBR\",\"cached_items\":[{\"sha256\":\"000ac7dc9366969db9d1e41810a3a27c747a7623535d856eecc2de86cfed80c7\"}],\"cohort\":\"rrf@0.00\",\"enabled\":true,\"installdate\":-1,\"lang\":\"en-US\",\"ping\":{\"r\":-2},\"targetingattributes\":{\"AppCohort\":\"rrf@0.00\",\"AppMajorVersion\":\"150\",\"AppRollout\":0,\"AppVersion\":\"150.0.4078.48\",\"IsInternalUser\":false,\"Priority\":false,\"Updater\":\"Omaha\",\"UpdaterVersion\":\"1.3.241.15\"},\"updatecheck\":{},\"version\":\"1.0.0.10\"},{\"appid"
		"\":\"ojblfafjmiikbkepnnolpgbbhejhlcim\",\"brand\":\"EPBR\",\"cached_items\":[{\"sha256\":\"2d2f683649600db91050fb41cd9ffea403ae024de38a0647b18e7f6106f6c55d\"}],\"cohort\":\"rrf@0.18\",\"enabled\":true,\"installdate\":-1,\"lang\":\"en-US\",\"ping\":{\"r\":-2},\"targetingattributes\":{\"AppCohort\":\"rrf@0.18\",\"AppMajorVersion\":\"150\",\"AppRollout\":0.18,\"AppVersion\":\"150.0.4078.48\",\"IsInternalUser\":false,\"Priority\":false,\"Updater\":\"Omaha\",\"UpdaterVersion\":\"1.3.241.15\"},\""
		"updatecheck\":{},\"version\":\"4.10.2934.0\"},{\"appid\":\"ahmaebgpfccdhgidjaidaoojjcijckba\",\"brand\":\"EPBR\",\"cached_items\":[{\"sha256\":\"07e0ad6da3d30a27962c6e09da9798ba1745856eaad71a036e2f639e93ea0b27\"}],\"cohort\":\"rrf@0.01\",\"enabled\":true,\"installdate\":-1,\"lang\":\"en-US\",\"ping\":{\"r\":-2},\"targetingattributes\":{\"AppCohort\":\"rrf@0.01\",\"AppMajorVersion\":\"150\",\"AppRollout\":0.01,\"AppVersion\":\"150.0.4078.48\",\"IsInternalUser\":false,\"Priority\":false,\"Updater\""
		":\"Omaha\",\"UpdaterVersion\":\"1.3.241.15\"},\"updatecheck\":{},\"version\":\"3.2.0.0\"},{\"appid\":\"pghocgajpebopihickglahgebcmkcekh\",\"brand\":\"EPBR\",\"cached_items\":[{\"sha256\":\"e49e08605c0aef671657dd880b748c1d0cc4887972b65a68e40e93b329056e51\"}],\"cohort\":\"rrf@0.98\",\"enabled\":true,\"installdate\":-1,\"lang\":\"en-US\",\"ping\":{\"r\":-2},\"targetingattributes\":{\"AppCohort\":\"rrf@0.98\",\"AppMajorVersion\":\"150\",\"AppRollout\":0.98,\"AppVersion\":\"150.0.4078.48\",\""
		"IsInternalUser\":false,\"Priority\":false,\"Updater\":\"Omaha\",\"UpdaterVersion\":\"1.3.241.15\"},\"updatecheck\":{},\"version\":\"3.0.0.18\"},{\"appid\":\"kmkacjgmmfchkbeglfbjjeidfckbnkca\",\"brand\":\"EPBR\",\"cached_items\":[{\"sha256\":\"e51d3f4ef39e9104ec54e50dda09696dc25e190990c201a202292cc0ce740397\"}],\"cohort\":\"rrf@0.82\",\"enabled\":true,\"installdate\":-1,\"lang\":\"en-US\",\"ping\":{\"r\":-2},\"targetingattributes\":{\"AppCohort\":\"rrf@0.82\",\"AppMajorVersion\":\"150\",\""
		"AppRollout\":0.82,\"AppVersion\":\"150.0.4078.48\",\"IsInternalUser\":false,\"Priority\":false,\"Updater\":\"Omaha\",\"UpdaterVersion\":\"1.3.241.15\"},\"updatecheck\":{},\"version\":\"2026.6.5.1\"},{\"appid\":\"plbmmhnabegcabfbcejohgjpkamkddhn\",\"brand\":\"EPBR\",\"cached_items\":[{\"sha256\":\"1e1174204f8a0a13de2e224a1be882d2724a6fd13ba18a895fd5098fd5552460\"}],\"cohort\":\"rrf@0.34\",\"enabled\":true,\"installdate\":-1,\"lang\":\"en-US\",\"ping\":{\"r\":-2},\"targetingattributes\":{\""
		"AppCohort\":\"rrf@0.34\",\"AppMajorVersion\":\"150\",\"AppRollout\":0.34,\"AppVersion\":\"150.0.4078.48\",\"IsInternalUser\":false,\"Priority\":false,\"Updater\":\"Omaha\",\"UpdaterVersion\":\"1.3.241.15\"},\"updatecheck\":{},\"version\":\"3057\"},{\"appid\":\"gllimckfbolmioaaihpppacjccghejen\",\"brand\":\"EPBR\",\"cached_items\":[{\"sha256\":\"8d64e3a35ee2c3e0b9e33afd63069fdc917a5647dd1e20c5ead97955fb6979f9\"}],\"cohort\":\"rrf@0.18\",\"enabled\":true,\"installdate\":-1,\"lang\":\"en-US\",\"ping"
		"\":{\"r\":-2},\"targetingattributes\":{\"AppCohort\":\"rrf@0.18\",\"AppMajorVersion\":\"150\",\"AppRollout\":0.18,\"AppVersion\":\"150.0.4078.48\",\"IsInternalUser\":false,\"Priority\":false,\"Updater\":\"Omaha\",\"UpdaterVersion\":\"1.3.241.15\"},\"updatecheck\":{},\"version\":\"1.2.0.0\"},{\"appid\":\"ohjmcpfnpmlgfkommepbhamjmanldlae\",\"brand\":\"EPBR\",\"cached_items\":[{\"sha256\":\"77ab8c118fd534ab1cf48f984963d6d35ebf06580b0041ec7d594ce88561ad84\"}],\"cohort\":\"rrf@0.81\",\"enabled\":true,"
		"\"installdate\":-1,\"lang\":\"en-US\",\"ping\":{\"r\":-2},\"targetingattributes\":{\"AppCohort\":\"rrf@0.81\",\"AppMajorVersion\":\"150\",\"AppRollout\":0.81,\"AppVersion\":\"150.0.4078.48\",\"IsInternalUser\":false,\"Priority\":false,\"Updater\":\"Omaha\",\"UpdaterVersion\":\"1.3.241.15\"},\"updatecheck\":{},\"version\":\"2026.2.24.1\"},{\"appid\":\"eodcfhpdifcaamjndfbdfbbhjkjgbion\",\"brand\":\"EPBR\",\"cached_items\":[{\"sha256\":\""
		"df5bb9f2afeb58b7c813d43eaa32cf6b240e346614ec52425bb5ff323450cd51\"}],\"cohort\":\"rrf@0.77\",\"enabled\":true,\"installdate\":-1,\"lang\":\"en-US\",\"ping\":{\"r\":-2},\"targetingattributes\":{\"AppCohort\":\"rrf@0.77\",\"AppMajorVersion\":\"150\",\"AppRollout\":0.77,\"AppVersion\":\"150.0.4078.48\",\"IsInternalUser\":false,\"Priority\":false,\"Updater\":\"Omaha\",\"UpdaterVersion\":\"1.3.241.15\"},\"updatecheck\":{},\"version\":\"2026.5.28.1\"},{\"appid\":\"llmidpclgepbgbgoecnhcmgfhmfplfao\",\""
		"brand\":\"EPBR\",\"cached_items\":[{\"sha256\":\"e80f622c70a53adf94afc099c1c7af2a23df3c6b2c99f0d5f9b8f601b7be3064\"}],\"cohort\":\"rrf@0.51\",\"enabled\":true,\"installdate\":-1,\"lang\":\"en-US\",\"ping\":{\"r\":-2},\"targetingattributes\":{\"AppCohort\":\"rrf@0.51\",\"AppMajorVersion\":\"150\",\"AppRollout\":0.51,\"AppVersion\":\"150.0.4078.48\",\"IsInternalUser\":false,\"Priority\":false,\"Updater\":\"Omaha\",\"UpdaterVersion\":\"1.3.241.15\"},\"updatecheck\":{},\"version\":\"2.1.107.0\"},{\""
		"appid\":\"jpinkpebmplndiafioikiciobeafamld\",\"brand\":\"EPBR\",\"cached_items\":[{\"sha256\":\"f081de18a604e95a175eaf4dd91b35b7f17ad4de24ee2f20eeb034c979bbcccb\"}],\"cohort\":\"rrf@0.92\",\"enabled\":true,\"installdate\":-1,\"lang\":\"en-US\",\"ping\":{\"r\":-2},\"targetingattributes\":{\"AppCohort\":\"rrf@0.92\",\"AppMajorVersion\":\"150\",\"AppRollout\":0.92,\"AppVersion\":\"150.0.4078.48\",\"IsInternalUser\":false,\"Priority\":false,\"Updater\":\"Omaha\",\"UpdaterVersion\":\"1.3.241.15\"},\""
		"updatecheck\":{},\"version\":\"2025.10.7.5\"},{\"appid\":\"npbipokbgmclmkjhfjicdgnedhkocjpl\",\"brand\":\"EPBR\",\"cached_items\":[{\"sha256\":\"04fad2fb7a1c552147e0b471ede01a383d6bd5d027e9399c9eab28f402014517\"}],\"cohort\":\"rrf@0.15\",\"enabled\":true,\"installdate\":-1,\"lang\":\"en-US\",\"model_locale\":\"en\",\"ping\":{\"r\":-2},\"targetingattributes\":{\"AppCohort\":\"rrf@0.15\",\"AppMajorVersion\":\"150\",\"AppRollout\":0.15,\"AppVersion\":\"150.0.4078.48\",\"IsInternalUser\":false,\""
		"Priority\":false,\"Updater\":\"Omaha\",\"UpdaterVersion\":\"1.3.241.15\"},\"updatecheck\":{},\"version\":\"2026.3.5.5\"},{\"appid\":\"fmbfidpnnknmblionmcahabilfoageoe\",\"brand\":\"EPBR\",\"cached_items\":[{\"sha256\":\"5a8a5a5d1f948d724847c005c9875507c34e5b76e73192fc1f2d22605fd69bd7\"}],\"cohort\":\"rrf@0.81\",\"enabled\":true,\"installdate\":-1,\"lang\":\"en-US\",\"ping\":{\"r\":-2},\"targetingattributes\":{\"AppCohort\":\"rrf@0.81\",\"AppMajorVersion\":\"150\",\"AppRollout\":0.81,\"AppVersion\""
		":\"150.0.4078.48\",\"IsInternalUser\":false,\"Priority\":false,\"Updater\":\"Omaha\",\"UpdaterVersion\":\"1.3.241.15\"},\"updatecheck\":{},\"version\":\"2026.2.23.1\"},{\"appid\":\"kieecehchjjaaepgajdhcehijkehdenm\",\"brand\":\"EPBR\",\"cached_items\":[{\"sha256\":\"4b7abf853d9b54dce31f8438c15aea88288358bd641b2de617860019ca0d85d4\"}],\"cohort\":\"rrf@0.22\",\"enabled\":true,\"installdate\":-1,\"lang\":\"en-US\",\"ping\":{\"r\":-2},\"targetingattributes\":{\"AppCohort\":\"rrf@0.22\",\""
		"AppMajorVersion\":\"150\",\"AppRollout\":0.22,\"AppVersion\":\"150.0.4078.48\",\"IsInternalUser\":false,\"Priority\":false,\"Updater\":\"Omaha\",\"UpdaterVersion\":\"1.3.241.15\"},\"updatecheck\":{},\"version\":\"2026.6.16.1\"},{\"appid\":\"jcmcegpcehdchljeldgmmfbgcpnmgedo\",\"brand\":\"EPBR\",\"cached_items\":[{\"sha256\":\"53f073c4807c121c9b0e81e08e232d5a71f4628e61fdf2f881e06255fb181b6f\"}],\"cohort\":\"rrf@0.78\",\"enabled\":true,\"installdate\":-1,\"lang\":\"en-US\",\"ping\":{\"r\":-2},\""
		"targetingattributes\":{\"AppCohort\":\"rrf@0.78\",\"AppMajorVersion\":\"150\",\"AppRollout\":0.78,\"AppVersion\":\"150.0.4078.48\",\"IsInternalUser\":false,\"Priority\":false,\"Updater\":\"Omaha\",\"UpdaterVersion\":\"1.3.241.15\"},\"updatecheck\":{},\"version\":\"2026.7.1.2\"},{\"appid\":\"fppmbhmldokgmleojlplaaodlkibgikh\",\"brand\":\"EPBR\",\"cached_items\":[{\"sha256\":\"a81d1959892ae4180554347df1b97834abba2e1a5e6b9aeba000ecea26eabecc\"}],\"cohort\":\"rrf@0.65\",\"enabled\":true,\"installdate"
		"\":-1,\"lang\":\"en-US\",\"ping\":{\"r\":-2},\"targetingattributes\":{\"AppCohort\":\"rrf@0.65\",\"AppMajorVersion\":\"150\",\"AppRollout\":0.65,\"AppVersion\":\"150.0.4078.48\",\"IsInternalUser\":false,\"Priority\":false,\"Updater\":\"Omaha\",\"UpdaterVersion\":\"1.3.241.15\"},\"updatecheck\":{},\"version\":\"1.15.0.1\"},{\"appid\":\"lkkdlcloifjinapabfonaibjijloebfb\",\"brand\":\"EPBR\",\"cached_items\":[{\"sha256\":\"46364648a637a691a999905fca2d18e6589ff2819f37cab64c3cff8128522130\"}],\"cohort\""
		":\"rrf@0.21\",\"enabled\":true,\"installdate\":-1,\"lang\":\"en-US\",\"ping\":{\"r\":-2},\"targetingattributes\":{\"AppCohort\":\"rrf@0.21\",\"AppMajorVersion\":\"150\",\"AppRollout\":0.21,\"AppVersion\":\"150.0.4078.48\",\"IsInternalUser\":false,\"Priority\":false,\"Updater\":\"Omaha\",\"UpdaterVersion\":\"1.3.241.15\"},\"updatecheck\":{},\"version\":\"4.0.4.17\"},{\"appid\":\"eiihffpgcdgabdmcecnakaohbclgfbmb\",\"brand\":\"EPBR\",\"cached_items\":[{\"sha256\":\""
		"cdff9e6a793fd77b105ed2ef1bf1788c1820af7d6f283202385434487672be8f\"}],\"cohort\":\"rrf@0.88\",\"enabled\":true,\"installdate\":-1,\"lang\":\"en-US\",\"ping\":{\"r\":-2},\"targetingattributes\":{\"AppCohort\":\"rrf@0.88\",\"AppMajorVersion\":\"150\",\"AppRollout\":0.88,\"AppVersion\":\"150.0.4078.48\",\"IsInternalUser\":false,\"Priority\":false,\"Updater\":\"Omaha\",\"UpdaterVersion\":\"1.3.241.15\"},\"updatecheck\":{},\"version\":\"2026.3.4.1\"},{\"appid\":\"lfmeghnikdkbonehgjihjebgioakijgn\",\""
		"brand\":\"EPBR\",\"cached_items\":[{\"sha256\":\"017cd1932d44fa3f5b7dcfd7ace33af995856842862c48ffbdb1df11e661a0ee\"}],\"cohort\":\"rrf@0.05\",\"enabled\":true,\"installdate\":-1,\"lang\":\"en-US\",\"ping\":{\"r\":-2},\"targetingattributes\":{\"AppCohort\":\"rrf@0.05\",\"AppMajorVersion\":\"150\",\"AppRollout\":0.05,\"AppVersion\":\"150.0.4078.48\",\"IsInternalUser\":false,\"Priority\":false,\"Updater\":\"Omaha\",\"UpdaterVersion\":\"1.3.241.15\"},\"updatecheck\":{},\"version\":\"2.0.0.145\"},{\""
		"appid\":\"hjaimielcgmceiphgjjfddlgjklfpdei\",\"brand\":\"EPBR\",\"cached_items\":[{\"sha256\":\"a00289af85d31d698a0f6753b6ce67dbab4bdff639bde5fc588a5d5d8a3885d5\"}],\"cohort\":\"rrf@0.71\",\"enabled\":true,\"installdate\":-1,\"lang\":\"en-US\",\"ping\":{\"r\":-2},\"targetingattributes\":{\"AppCohort\":\"rrf@0.71\",\"AppMajorVersion\":\"150\",\"AppRollout\":0.71,\"AppVersion\":\"150.0.4078.48\",\"IsInternalUser\":false,\"Priority\":false,\"Updater\":\"Omaha\",\"UpdaterVersion\":\"1.3.241.15\"},\""
		"updatecheck\":{},\"version\":\"1.0.0.5\"},{\"appid\":\"pbdgbpmpeenomngainidcjmopnklimmf\",\"brand\":\"EPBR\",\"cached_items\":[{\"sha256\":\"b27bec7581505715364f132de1998818c82462dbf55a1f55f9b15e29e988d791\"}],\"cohort\":\"rrf@0.50\",\"enabled\":true,\"installdate\":-1,\"lang\":\"en-US\",\"ping\":{\"r\":-2},\"targetingattributes\":{\"AppCohort\":\"rrf@0.50\",\"AppMajorVersion\":\"150\",\"AppRollout\":0.5,\"AppVersion\":\"150.0.4078.48\",\"IsInternalUser\":false,\"Priority\":false,\"Updater\":\""
		"Omaha\",\"UpdaterVersion\":\"1.3.241.15\"},\"updatecheck\":{},\"version\":\"0.0.0.46\"},{\"accept_locale\":\"ENUS\",\"appid\":\"njaocnahcpjeeknehofkiijbojppiiki\",\"brand\":\"EPBR\",\"cohort\":\"rrf@0.06\",\"enabled\":true,\"installdate\":-1,\"lang\":\"en-US\",\"ping\":{\"r\":-2},\"targetingattributes\":{\"AppCohort\":\"rrf@0.06\",\"AppMajorVersion\":\"150\",\"AppRollout\":0.06,\"AppVersion\":\"150.0.4078.48\",\"IsInternalUser\":false,\"Priority\":false,\"Updater\":\"Omaha\",\"UpdaterVersion\":\""
		"1.3.241.15\"},\"updatecheck\":{},\"version\":\"0.0.0.0\"},{\"appid\":\"nmcnjaceoejcjmmnabjnmfpoanaengif\",\"brand\":\"EPBR\",\"cached_items\":[{\"sha256\":\"a9592ae40712c6cfdf7d142e2563ca4ec8f696cfe53e267ad0ea630c43beaa33\"}],\"cohort\":\"rrf@0.86\",\"enabled\":true,\"installdate\":-1,\"lang\":\"en-US\",\"ping\":{\"r\":-2},\"targetingattributes\":{\"AppCohort\":\"rrf@0.86\",\"AppMajorVersion\":\"150\",\"AppRollout\":0.86,\"AppVersion\":\"150.0.4078.48\",\"IsInternalUser\":false,\"Priority\":false,"
		"\"Updater\":\"Omaha\",\"UpdaterVersion\":\"1.3.241.15\"},\"updatecheck\":{},\"version\":\"2026.1.30.1\"},{\"appid\":\"cllppcmmlnkggcmljjfigkcigaajjmid\",\"brand\":\"EPBR\",\"cached_items\":[{\"sha256\":\"38b9a60260c000df8eadd64719d86020e30480df9afb893e60b5ef7d780616a5\"}],\"cohort\":\"rrf@0.44\",\"enabled\":true,\"installdate\":-1,\"lang\":\"en-US\",\"ping\":{\"r\":-2},\"targetingattributes\":{\"AppCohort\":\"rrf@0.44\",\"AppMajorVersion\":\"150\",\"AppRollout\":0.44,\"AppVersion\":\""
		"150.0.4078.48\",\"IsInternalUser\":false,\"Priority\":false,\"Updater\":\"Omaha\",\"UpdaterVersion\":\"1.3.241.15\"},\"updatecheck\":{},\"version\":\"128.18367.18366.1\"},{\"appid\":\"jbfaflocpnkhbgcijpkiafdpbjkedane\",\"brand\":\"EPBR\",\"cohort\":\"rrf@0.90\",\"enabled\":true,\"installdate\":-1,\"lang\":\"en-US\",\"ping\":{\"r\":-2},\"targetingattributes\":{\"AppCohort\":\"rrf@0.90\",\"AppMajorVersion\":\"150\",\"AppRollout\":0.9,\"AppVersion\":\"150.0.4078.48\",\"IsInternalUser\":false,\""
		"Priority\":false,\"Updater\":\"Omaha\",\"UpdaterVersion\":\"1.3.241.15\"},\"updatecheck\":{},\"version\":\"1.0.0.37\"},{\"appid\":\"mkcgfaeepibomfapiapjaceihcojnphg\",\"brand\":\"EPBR\",\"cohort\":\"rrf@0.50\",\"enabled\":true,\"installdate\":-1,\"lang\":\"en-US\",\"ping\":{\"r\":-2},\"targetingattributes\":{\"AppCohort\":\"rrf@0.50\",\"AppMajorVersion\":\"150\",\"AppRollout\":0.5,\"AppVersion\":\"150.0.4078.48\",\"IsInternalUser\":false,\"Priority\":false,\"Updater\":\"Omaha\",\"UpdaterVersion\""
		":\"1.3.241.15\"},\"updatecheck\":{},\"version\":\"0.0.0.0\"},{\"appid\":\"gghpafdlgdjgkjfihkmbhlkmdoagjnom\",\"brand\":\"EPBR\",\"cached_items\":[{\"sha256\":\"62c2681c773d6b8cb56acc5ab5856ae85b710946046b9018d7e9629ad0ab486b\"}],\"cohort\":\"rrf@0.17\",\"enabled\":true,\"installdate\":-1,\"lang\":\"en-US\",\"ping\":{\"r\":-2},\"targetingattributes\":{\"AppCohort\":\"rrf@0.17\",\"AppMajorVersion\":\"150\",\"AppRollout\":0.17,\"AppVersion\":\"150.0.4078.48\",\"IsInternalUser\":false,\"Priority\""
		":false,\"Updater\":\"Omaha\",\"UpdaterVersion\":\"1.3.241.15\"},\"updatecheck\":{},\"version\":\"2026.5.13.1\"},{\"appid\":\"pdfjdcjjjegpclfiilihfkmdfndkneei\",\"brand\":\"EPBR\",\"cached_items\":[{\"sha256\":\"8a5ae7ba183c6349a26d5b81ca4379b1e9e147ecfdc7d3bd0e7d205410e32fb4\"}],\"cohort\":\"rrf@0.62\",\"enabled\":true,\"installdate\":-1,\"lang\":\"en-US\",\"ping\":{\"r\":-2},\"targetingattributes\":{\"AppCohort\":\"rrf@0.62\",\"AppMajorVersion\":\"150\",\"AppRollout\":0.62,\"AppVersion\":\""
		"150.0.4078.48\",\"IsInternalUser\":false,\"Priority\":false,\"Updater\":\"Omaha\",\"UpdaterVersion\":\"1.3.241.15\"},\"updatecheck\":{},\"version\":\"2025.7.24.0\"}],\"arch\":\"x64\",\"dedup\":\"cr\",\"domainjoined\":false,\"hw\":{\"avx\":1,\"physmemory\":31,\"sse\":1,\"sse2\":1,\"sse3\":1,\"sse41\":1,\"sse42\":1,\"ssse3\":1},\"ismachine\":1,\"os\":{\"arch\":\"x86_64\",\"platform\":\"Windows\",\"version\":\"10.0.26200.8655\"},\"prodversion\":\"150.0.4078.48\",\"protocol\":\"4.0\",\"requestid\":\""
		"{aa4d9920-cbbc-4ef7-8ebd-ebfb40c9a245}\",\"sessionid\":\"{12362c54-1330-4510-b2d7-0862b7217eb8}\",\"updaters\":{\"autoupdatecheckenabled\":true,\"ismachine\":1,\"lastchecked\":0,\"laststarted\":0,\"name\":\"Omaha\",\"updatepolicy\":-1,\"version\":\"1.3.241.15\"},\"updaterversion\":\"150.0.4078.48\"}}", 
		LAST);

	web_custom_request("3", 
		"URL=https://nav-edge.smartscreen.microsoft.com/api/browser/edge/navigate/3", 
		"Method=POST", 
		"Resource=0", 
		"RecContentType=application/json", 
		"Referer=", 
		"Snapshot=t27.inf", 
		"Mode=HTML", 
		"EncType=application/json; charset=utf-8", 
		"Body={\"userAgent\":\"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36 Edg/150.0.0.0\",\"redirectChain\":[],\"enhancedRedirectChain\":{\"redirectSource\":null,\"referrerChain\":[]},\"identity\":{\"user\":{\"locale\":\"en-US\"},\"device\":{\"id\":null,\"customId\":\"7ef6a2b3-1480-4e92-823c-d9f6b2467862\",\"onlineIdTicket\":\"t=GwD2Ad9tBAAUACvdRm27aTQoBWtI3fAPXDuVCyUOZgAAEAZJvpZluaP0As/VkUSwbALAATGGoyOiHeN6lVEod1SAwY+IiWlXv+J6Hyn3rmuNGV+"
		"EU5i9qALHfyndcgaB75qHCvkYL77iiembIEqb3FRgGpXs+k4fw4AsXnafDvc43eNvvS6zS6LV+hOPEew0mDVd/m78g+AEBJHXW+gYpNclS8JQEmREN1CidQLGjDFw5fDNNj5UNF5JYi2U/anHwk9TWxIVRqz3ztSp4zVEQzSskBlGBlcRRDWXZ11+iQAMvczGUC9EgW9wAySKVMD8H4M4E8BJ1kXObESnfLNdxC9jk5ff7lJGXefwKml4YGMpxiBA1G3/hsxVfI2yq9sWMMBOXorxD2aZgtRHGArV7cahCzqaKJ9aKfVg81Rsh+cFc23Aw+6fxCV50CTRRozTWRqxw5fBqoyrMLX/AE09zIETpcFhnPWjpDeERy1vwGQS0EdUmcu9dzgkiQct7sVe2rMN7nv77OlMawSIvQGf43OaRpPhLHsDY3wLZuLFF22X7aOm0r3wL6pQyJVIE2UUIWaJ/qLdtB+"
		"lLyJiBXwzTzgYu8vU25nIg0RLOihWzWk6qF48wEECYYYbcFhfHGOhp06HHiWCdzRXhBWfBYit3S8Sfpz6AQ==&p=\",\"family\":3,\"locale\":\"en-US\",\"osVersion\":\"10.0.26200.8655.ge_release\",\"browser\":{\"internetExplorer\":\"9.11.26100.0\"},\"netJoinStatus\":2,\"enterprise\":{},\"cloudSku\":false,\"architecture\":9},\"caller\":{\"locale\":\"en-US\",\"name\":\"\",\"version\":\"150.0.4078.48 (Official build) \"},\"client\":{\"version\":\"281483737432064\",\"data\":{\"topTraffic\":\"638004170464094982\",\""
		"customSynchronousLookupUris\":\"0\",\"edgeSettings\":\"2.0-a82cb2897a8bf9445d68dcc2be05af89ad4b2fda1fddb2952693be7cd5353ad3\",\"customSettings\":\"F95BA787499AB4FA9EFFF472CE383A14\"}}},\"config\":{\"user\":{\"uriReputation\":{\"enforcedByPolicy\":false,\"level\":\"warn\"}},\"device\":{\"appControl\":{\"level\":\"anywhere\"},\"appReputation\":{\"enforcedByPolicy\":false,\"level\":\"warn\"}}},\"destination\":{\"uri\":\"https://www.tangerine.ca/en/personal\",\"ip\":\"23.58.187.247\"},\"type\":\"top\""
		",\"forceServiceDetermination\":false,\"correlationId\":\"b151ecda-2608-45de-a89e-efd4523e4fad\",\"synchronous\":false}", 
		LAST);

	web_url("personal", 
		"URL=https://www.tangerine.ca/en/personal", 
		"Resource=0", 
		"RecContentType=text/html", 
		"Referer=", 
		"Snapshot=t28.inf", 
		"Mode=HTML", 
		LAST);

	web_url("V1Profile_2", 
		"URL=https://substrate.office.com/profileb2/v2.0/me/V1Profile", 
		"Resource=0", 
		"RecContentType=application/json", 
		"Referer=", 
		"Snapshot=t29.inf", 
		"Mode=HTML", 
		LAST);

	web_custom_request("command_2", 
		"URL=https://edge.microsoft.com/sync/v1/feeds/me/syncEntities/command/?client=Chromium&client_id=fG%2BQBAAE43Au5Ym6F%2FeYCg%3D%3D", 
		"Method=POST", 
		"Resource=0", 
		"RecContentType=application/octet-stream", 
		"Referer=", 
		"Snapshot=t30.inf", 
		"ContentEncoding=gzip", 
		"Mode=HTML", 
		"EncType=application/octet-stream", 
		"BodyBinary=\n\\x18fG+QBAAE43Au5Ym6F/eYCg==\\x10c\\x18\\x01\"\\x9F\\x10\n\\xC3\\x01\n$50f5ec63-5b90-4636-952b-3724b247fdeb \\xED\\xDA\\x8A\\xA3\\xF33(\\x8A\\xEF\\x80\\xA5\\xF330\\x93\\x95\\xE4\\xB0\\x853:)profile.edge_user_with_non_zero_passwords\\x90\\x01\\x00\\xAA\\x015\\xB2\\xB4\\x121\n)profile.edge_user_with_non_zero_passwords\\x12\\x04true\\xBA\\x01\\x1CMBpLcJqw56uEssjAtHh8+lFm6N4=\\xC2>\\x00\n\\xCB\\x01\n$bb04951e-7ed7-4ad3-97ef-022fb0a24e41 \\xDC\\xBF\\x95\\x81\\xF13"
		"(\\xB1\\xB1\\xF7\\xA4\\xF330\\x8E\\xF7\\xD9\\xE9\\xE40:\\x13profile.network_pbs\\x90\\x01\\x00\\xAA\\x01S\\xB2\\xB4\\x12O\n\\x13profile.network_pbs\\x128{\"f98a555e\":{\"last_updated\":\"13427767787697126\",\"pb\":1}}\\xBA\\x01\\x1CKx0h0OM/f/g5lWtAv8REcQOg8C8=\\xC2>\\x00\n\\xF8\\x06\n$5d948db1-d2ec-4d5e-b9e3-86358a032d54 \\xEE\\xDA\\x8A\\xA3\\xF33(\\xF2\\xAC\\x82\\xA5\\xF330\\xA2\\xD8\\xC9\\xA3\\xC53:\nWEIPENG-X1\\x90\\x01\\x00\\xAA\\x01\\x88\\x06\\xD2\\xB9K\\x83\\x06\n\\x18fG+QBAAE43Au5Ym6F/eYCg="
		"=\\x12\nWEIPENG-X1\\x18\\x01\"SChrome WIN 150.0.4078.48 (6362dfa84aa4f30c18c60ac12387d02753f37dc6) channel(stable)*\r150.0.4078.48:$acbf55b4-e729-4318-a9c1-005d5736ae36@\\xF2\\xAC\\x82\\xA5\\xF33J\\x81\\x02\\x08\\x01\\x10\\x00 \\x00\\xCA>3{\"lastTimeUpdated\":\"13427767967346441\",\"segment\":3}\\xD2>\\xC1\\x01{\"dndSignals\":{\"execution_time\":\"13420583455077548\",\"is_ready\":true,\"model_version\":7,\"output\":[6.0,3.0,3.0,3.0,1.0,3.0,3.0,1.0,3.0,6.0],\"segment_id\":535},\"lastTimeUpdated\":"
		"\"13427767967346444\"}Z\n21KC009XUSb\\x06LENOVOh\\xA0\\x0Br\\x94\\x02\n\\xC9\\x01ecm:Rb1RT+5wrbtaWK7gBHVT1A==$+LRBtdF1aijYudCvrBKN2PFGkBHUBCHKRSPj7/j7QO8rAzMQrHlEc62zhWZ/1rn47Fui1ILvP2xLCCs0XR2Q3/Z7Em3jnTvAh0R3cocqcxu3r+eGe4qsbK1NArvd0ywNc94gPvW5nBiXAIV8s9B6eILtNJne0etZvjEuKGLXrXA=\\x10\\x88\\x81\\x02\\x10\\xC6\\xA6\\x02\\x10\\xB1\\xE6\\x02\\x10\\xCF\\xF3\\x03\\x10\\xF1\\xF7\\x01\\x10\\xF7\\xF7\\x02\\x10\\x9F\\xEF\\x05\\x10\\xEB\\x95\t\\x10\\x9A\\xB7\t\\x10\\xFC\\xDE$\\x10\\xC9\\x8B)"
		"\\x10\\x91\\xEB:\\x10\\xCA\\xAA=\\x10\\xAB\\xD26\\x10\\xD0\\xAF:\\x10\\xA9\\xF0O\\x10\\xE4\\x92t\\x10\\x81\\xF5\\x02\\x8A\\x01\\x0F\n\r150.0.4078.48\\x98\\x01\\x01\\xA0\\x01\\x01\\xBA\\x01\\x1CYpJcWXUIqUFea7vOzwR44E5yRbA=\\xC2>\\x00\\x12\\x18fG+QBAAE43Au5Ym6F/eYCg==\"\\xF0\\x03\\x08\\x88\\x81\\x02\\x08\\xC6\\xA6\\x02\\x08\\xB1\\xE6\\x02\\x08\\xCF\\xF3\\x03\\x08\\xF1\\xF7\\x01\\x08\\xF7\\xF7\\x02\\x08\\xC7\\x87\\x03\\x08\\x9F\\xEF\\x05\\x08\\xEB\\x95\t\\x08\\x9A\\xB7\t\\x08\\xEE\\xF7"
		"!\\x08\\xFC\\xDE$\\x08\\xC9\\x8B)\\x08\\x91\\xEB:\\x08\\xCA\\xAA=\\x08\\xAB\\xD26\\x08\\xD0\\xAF:\\x08\\xA9\\xF0O\\x08\\xE4\\x92t\\x08\\x81\\xF5\\x02\\x18\\x00 \\x00*\\xC9\\x01ecm:S10KhfE1uB8fCAuftVjUmQ==$o0gv4lquc9B5i9BAkidp/69UGc6YLwZ46k+fGZ8Ad1a1Ou2Ox34P3u3mNnpSb7RLsaxwX9xYx/+HuAXTg1TEeOaRwpElr1drs8CkZLvGBUQxL/6YfA4FR1p2gb0bMHpLrt9vlr/KOPVfDStQmj+8iB5O86X4mZ6YUIxY1c5PSUE=0\\x00:\\xC9\\x01ecm:S10KhfE1uB8fCAuftVjUmQ==$o0gv4lquc9B5i9BAkidp/69UGc6YLwZ46k+fGZ8Ad1a1Ou2Ox34P3u3mNnpSb7RLsaxwX9xYx/+"
		"HuAXTg1TEeOaRwpElr1drs8CkZLvGBUQxL/6YfA4FR1p2gb0bMHpLrt9vlr/KOPVfDStQmj+8iB5O86X4mZ6YUIxY1c5PSUE=@\\x012\\x80\\x02aXz?3Wm$\"-[<<Msz@Ir/99kZ983gE;q6|)RXs,TK2YhFQYI=2'TU$`GzMG;[AE%pe)EV.Uaw[{SPtX$#=Qp(uc@@$/|0T1H\\\\wb%+/%p$7y[')#'.Uh<.S%%ej$Hs0D{~!V7}m0bAmF8:y\"fn&S)c`/PYl*`44K\"#z$_7wX9.U}YJ7Ob~@6RuL>lrJ{z<zi$+l49r`<#>j4@78{^Mj.%Vj|'{Rw[\"cf+k\"Q3ckgN0^xN\"G~;I+#OyKmqpSNA4cw,L:\\x1FProductionEnvironmentDefinitionR\\x06\\x10\\x01\\x18\\x00 \\x00Z\\x00b\ndummytokenj\\x02\\x10\\x01r\\x1Cchr:fG+"
		"QBAAE43Au5Ym6F/eYCg==", 
		LAST);

	lr_think_time(4);

	web_url("personal_2", 
		"URL=https://www.tangerine.ca/en/personal", 
		"Resource=0", 
		"RecContentType=text/html", 
		"Referer=", 
		"Snapshot=t31.inf", 
		"Mode=HTML", 
		LAST);

	web_custom_request("3_2", 
		"URL=https://nav-edge.smartscreen.microsoft.com/api/browser/edge/navigate/3", 
		"Method=POST", 
		"Resource=0", 
		"RecContentType=application/json", 
		"Referer=", 
		"Snapshot=t32.inf", 
		"Mode=HTML", 
		"EncType=application/json; charset=utf-8", 
		"Body={\"userAgent\":\"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36 Edg/150.0.0.0\",\"redirectChain\":[],\"enhancedRedirectChain\":{\"redirectSource\":null,\"referrerChain\":[]},\"identity\":{\"user\":{\"locale\":\"en-US\"},\"device\":{\"id\":null,\"customId\":\"5ac5d8d1-aa99-4e3d-93e2-1e1fe3937691\",\"onlineIdTicket\":\"t=GwD2Ad9tBAAUACvdRm27aTQoBWtI3fAPXDuVCyUOZgAAEAZJvpZluaP0As/VkUSwbALAATGGoyOiHeN6lVEod1SAwY+IiWlXv+J6Hyn3rmuNGV+"
		"EU5i9qALHfyndcgaB75qHCvkYL77iiembIEqb3FRgGpXs+k4fw4AsXnafDvc43eNvvS6zS6LV+hOPEew0mDVd/m78g+AEBJHXW+gYpNclS8JQEmREN1CidQLGjDFw5fDNNj5UNF5JYi2U/anHwk9TWxIVRqz3ztSp4zVEQzSskBlGBlcRRDWXZ11+iQAMvczGUC9EgW9wAySKVMD8H4M4E8BJ1kXObESnfLNdxC9jk5ff7lJGXefwKml4YGMpxiBA1G3/hsxVfI2yq9sWMMBOXorxD2aZgtRHGArV7cahCzqaKJ9aKfVg81Rsh+cFc23Aw+6fxCV50CTRRozTWRqxw5fBqoyrMLX/AE09zIETpcFhnPWjpDeERy1vwGQS0EdUmcu9dzgkiQct7sVe2rMN7nv77OlMawSIvQGf43OaRpPhLHsDY3wLZuLFF22X7aOm0r3wL6pQyJVIE2UUIWaJ/qLdtB+"
		"lLyJiBXwzTzgYu8vU25nIg0RLOihWzWk6qF48wEECYYYbcFhfHGOhp06HHiWCdzRXhBWfBYit3S8Sfpz6AQ==&p=\",\"family\":3,\"locale\":\"en-US\",\"osVersion\":\"10.0.26200.8655.ge_release\",\"browser\":{\"internetExplorer\":\"9.11.26100.0\"},\"netJoinStatus\":2,\"enterprise\":{},\"cloudSku\":false,\"architecture\":9},\"caller\":{\"locale\":\"en-US\",\"name\":\"\",\"version\":\"150.0.4078.48 (Official build) \"},\"client\":{\"version\":\"281483737432064\",\"data\":{\"topTraffic\":\"638004170464094982\",\""
		"customSynchronousLookupUris\":\"0\",\"edgeSettings\":\"2.0-a82cb2897a8bf9445d68dcc2be05af89ad4b2fda1fddb2952693be7cd5353ad3\",\"customSettings\":\"F95BA787499AB4FA9EFFF472CE383A14\"}}},\"config\":{\"user\":{\"uriReputation\":{\"enforcedByPolicy\":false,\"level\":\"warn\"}},\"device\":{\"appControl\":{\"level\":\"anywhere\"},\"appReputation\":{\"enforcedByPolicy\":false,\"level\":\"warn\"}}},\"destination\":{\"uri\":\"https://www.tangerine.ca/en/personal\",\"ip\":null},\"type\":\"top\",\""
		"forceServiceDetermination\":false,\"correlationId\":\"44aab5ba-0a21-49cf-9051-8facf2fb28df\",\"synchronous\":false}", 
		LAST);

	lr_think_time(4);

	web_custom_request("command_3", 
		"URL=https://edge.microsoft.com/sync/v1/feeds/me/syncEntities/command/?client=Chromium&client_id=fG%2BQBAAE43Au5Ym6F%2FeYCg%3D%3D", 
		"Method=POST", 
		"Resource=0", 
		"RecContentType=application/octet-stream", 
		"Referer=", 
		"Snapshot=t33.inf", 
		"ContentEncoding=gzip", 
		"Mode=HTML", 
		"EncType=application/octet-stream", 
		"BodyBinary=\n\\x18fG+QBAAE43Au5Ym6F/eYCg==\\x10c\\x18\\x01\"\\x8B\r\n\\xF8\\x06\n$5d948db1-d2ec-4d5e-b9e3-86358a032d54 \\x80\\xD3\\x85\\xA5\\xF33(\\xCC\\xEE\\x85\\xA5\\xF330\\xA2\\xD8\\xC9\\xA3\\xC53:\nWEIPENG-X1\\x90\\x01\\x00\\xAA\\x01\\x88\\x06\\xD2\\xB9K\\x83\\x06\n\\x18fG+QBAAE43Au5Ym6F/eYCg==\\x12\nWEIPENG-X1\\x18\\x01\"SChrome WIN 150.0.4078.48 (6362dfa84aa4f30c18c60ac12387d02753f37dc6) channel(stable)*\r150.0.4078.48"
		":$acbf55b4-e729-4318-a9c1-005d5736ae36@\\xCC\\xEE\\x85\\xA5\\xF33J\\x81\\x02\\x08\\x01\\x10\\x00 \\x00\\xCA>3{\"lastTimeUpdated\":\"13427768024908362\",\"segment\":3}\\xD2>\\xC1\\x01{\"dndSignals\":{\"execution_time\":\"13420583455077548\",\"is_ready\":true,\"model_version\":7,\"output\":[6.0,3.0,3.0,3.0,1.0,3.0,3.0,1.0,3.0,6.0],\"segment_id\":535},\"lastTimeUpdated\":\"13427768024908364\"}Z\n21KC009XUSb\\x06LENOVOh\\xA0\\x0Br\\x94\\x02\n\\xC9\\x01ecm:Rb1RT+5wrbtaWK7gBHVT1A==$+"
		"LRBtdF1aijYudCvrBKN2PFGkBHUBCHKRSPj7/j7QO8rAzMQrHlEc62zhWZ/1rn47Fui1ILvP2xLCCs0XR2Q3/Z7Em3jnTvAh0R3cocqcxu3r+eGe4qsbK1NArvd0ywNc94gPvW5nBiXAIV8s9B6eILtNJne0etZvjEuKGLXrXA=\\x10\\x88\\x81\\x02\\x10\\xC6\\xA6\\x02\\x10\\xB1\\xE6\\x02\\x10\\xCF\\xF3\\x03\\x10\\xF1\\xF7\\x01\\x10\\xF7\\xF7\\x02\\x10\\x9F\\xEF\\x05\\x10\\xEB\\x95\t\\x10\\x9A\\xB7\t\\x10\\xFC\\xDE$\\x10\\xC9\\x8B)\\x10\\x91\\xEB:\\x10\\xCA\\xAA=\\x10\\xAB\\xD26\\x10\\xD0\\xAF"
		":\\x10\\xA9\\xF0O\\x10\\xE4\\x92t\\x10\\x81\\xF5\\x02\\x8A\\x01\\x0F\n\r150.0.4078.48\\x98\\x01\\x01\\xA0\\x01\\x01\\xBA\\x01\\x1CYpJcWXUIqUFea7vOzwR44E5yRbA=\\xC2>\\x00\\x12\\x18fG+QBAAE43Au5Ym6F/eYCg==\"\\xF0\\x03\\x08\\x88\\x81\\x02\\x08\\xC6\\xA6\\x02\\x08\\xB1\\xE6\\x02\\x08\\xCF\\xF3\\x03\\x08\\xF1\\xF7\\x01\\x08\\xF7\\xF7\\x02\\x08\\xC7\\x87\\x03\\x08\\x9F\\xEF\\x05\\x08\\xEB\\x95\t\\x08\\x9A\\xB7\t\\x08\\xEE\\xF7!\\x08\\xFC\\xDE$\\x08\\xC9\\x8B)\\x08\\x91\\xEB:\\x08\\xCA\\xAA="
		"\\x08\\xAB\\xD26\\x08\\xD0\\xAF:\\x08\\xA9\\xF0O\\x08\\xE4\\x92t\\x08\\x81\\xF5\\x02\\x18\\x00 \\x00*\\xC9\\x01ecm:S10KhfE1uB8fCAuftVjUmQ==$o0gv4lquc9B5i9BAkidp/69UGc6YLwZ46k+fGZ8Ad1a1Ou2Ox34P3u3mNnpSb7RLsaxwX9xYx/+HuAXTg1TEeOaRwpElr1drs8CkZLvGBUQxL/6YfA4FR1p2gb0bMHpLrt9vlr/KOPVfDStQmj+8iB5O86X4mZ6YUIxY1c5PSUE=0\\x00:\\xC9\\x01ecm:S10KhfE1uB8fCAuftVjUmQ==$o0gv4lquc9B5i9BAkidp/69UGc6YLwZ46k+fGZ8Ad1a1Ou2Ox34P3u3mNnpSb7RLsaxwX9xYx/+HuAXTg1TEeOaRwpElr1drs8CkZLvGBUQxL/6YfA4FR1p2gb0bMHpLrt9vlr/"
		"KOPVfDStQmj+8iB5O86X4mZ6YUIxY1c5PSUE=@\\x012\\x80\\x02zjkkxe6\"HvSgo*4';d1b}ck-yx<zS8S6t&#]mIK.`rQU&x6`#YvqJ\\\\J#cQMBxK5(q (QDKC>]E&]jRXrm?kJ~+VA9K]%pzYt)_N_f1!LWe:M{j`zU^ARn]k:f*XDr\\\\3:]CiUBNI8&.wy_zm@rtM8Drm*wmV%vBWjAe5K>/4y{y<shUo{Yd)_(Q%|wcW_wj*;5(v`:D7*2]v4-5mYuLam8tz[gi13$l(,8lZi//w#]]X}]{VLrKp?KR>bg]5S$,E\":\\x1FProductionEnvironmentDefinitionR\\x96\\x01\nB\\x12@8\\x00@\\x00R\\x02\\x10\\x01`\\x0C\\x92\\x03\\x18I7p5Hkjmv8seONCjNx2sLG.1\\x92\\x03\\x18F3dLocFmNyEUDGw4Ldx4jM.1\n"
		"\\x04\\x18\\xC6\\xA6\\x02\n\\x04\\x18\\x9A\\xB7\t\n\\x04\\x18\\x9A\\xB7\t\\x10\\x01\\x18\\x00 \\x00(\\x88\\x81\\x02(\\xC6\\xA6\\x02(\\xB1\\xE6\\x02(\\xF7\\xF7\\x02(\\x9F\\xEF\\x05(\\xEB\\x95\t(\\xFC\\xDE$(\\xC9\\x8B)(\\x91\\xEB:(\\xCA\\xAA=(\\xAB\\xD26(\\xD0\\xAF:(\\xE4\\x92t(\\x81\\xF5\\x020\\x01Z\\x00b\ndummytokenj\\x02\\x10\\x01r\\x1Cchr:fG+QBAAE43Au5Ym6F/eYCg==", 
		LAST);

	return 0;
}