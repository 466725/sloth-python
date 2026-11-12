Action()
{

	web_set_sockets_option("SSL_VERSION", "AUTO");

	web_set_max_html_param_len("612");

	web_add_auto_header("Sec-Fetch-Dest", 
		"empty");

	web_add_auto_header("Sec-Fetch-Mode", 
		"no-cors");

	web_add_auto_header("Sec-Fetch-Site", 
		"none");

	web_add_auto_header("Sec-Fetch-Storage-Access", 
		"active");

	web_add_auto_header("Sec-Mesh-Client-Arch", 
		"x86_64");

	web_add_auto_header("Sec-Mesh-Client-Edge-Channel", 
		"stable");

	web_add_auto_header("Sec-Mesh-Client-Edge-Version", 
		"157.0.4341.46");

	web_add_auto_header("Sec-Mesh-Client-OS", 
		"Windows");

	web_add_auto_header("Sec-Mesh-Client-OS-Version", 
		"10.0.26300");

	web_add_auto_header("Sec-Mesh-Client-WebView", 
		"0");

	web_url("blocklist", 
		"URL=https://edge.microsoft.com/abusiveadblocking/api/v1/blocklist", 
		"Resource=0", 
		"RecContentType=application/json", 
		"Referer=", 
		"Snapshot=t1.inf", 
		"Mode=HTML", 
		LAST);

	web_add_cookie("MC1=GUID%3D55dad4d1f9de4196a829af23c0d83dec%26HASH%3D55da%26LV%3D202610%26V%3D4%26LU%3D1790878562587; DOMAIN=edge.microsoft.com");

	web_url("aad", 
		"URL=https://edge.microsoft.com/identity/api/v4/aad", 
		"Resource=0", 
		"RecContentType=application/json", 
		"Referer=", 
		"Snapshot=t2.inf", 
		"Mode=HTML", 
		LAST);

	web_revert_auto_header("Sec-Mesh-Client-Arch");

	web_revert_auto_header("Sec-Mesh-Client-Edge-Channel");

	web_revert_auto_header("Sec-Mesh-Client-Edge-Version");

	web_revert_auto_header("Sec-Mesh-Client-OS");

	web_revert_auto_header("Sec-Mesh-Client-OS-Version");

	web_revert_auto_header("Sec-Mesh-Client-WebView");

	web_add_header("X-ECS-Client-Last-Telemetry-Events", 
		"ecs_client_library_name=IntuneDesktopMAM,ecs_client_app_name=com.microsoft.edge,ecs_client_version=2.4.2.0");

	web_url("1.0", 
		"URL=https://config.edge.skype.com/config/v1/Intune/1.0?agents=CLI_DesktopMAM&appId=com.microsoft.edge&appVersion=157.0.4341.46&clientId=8fcda4f9-0248-46ea-8edc-3d78ced6a6f5&osType=windows&osVersion_version=10.0.26300.9974", 
		"Resource=0", 
		"RecContentType=application/json", 
		"Referer=", 
		"Snapshot=t3.inf", 
		"Mode=HTML", 
		LAST);

	web_revert_auto_header("Sec-Fetch-Storage-Access");

	web_add_header("X-Microsoft-Update-AppId", 
		"jmjflgjpcpepeafmmgdpfkogkghcpiha");

	web_add_header("X-Microsoft-Update-Service-Cohort", 
		"8610");

	web_add_header("X-Microsoft-Update-Updater", 
		"msedgecrx-157.0.4341.46");

	web_add_header("MS-CV", 
		"bbXIZktcJ94yTk7a7ZqTGy");

	web_add_auto_header("Sec-Mesh-Client-Arch", 
		"x86_64");

	web_add_auto_header("Sec-Mesh-Client-Edge-Channel", 
		"stable");

	web_add_auto_header("Sec-Mesh-Client-Edge-Version", 
		"157.0.4341.46");

	web_add_auto_header("Sec-Mesh-Client-OS", 
		"Windows");

	web_add_auto_header("Sec-Mesh-Client-OS-Version", 
		"10.0.26300");

	web_add_auto_header("Sec-Mesh-Client-WebView", 
		"0");

	web_add_header("X-Client-Data", 
		"CKxN");

	web_add_auto_header("X-Microsoft-Update-Interactivity", 
		"bg");

	web_custom_request("crx", 
		"URL=https://edge.microsoft.com/extensionwebstorebase/v1/crx", 
		"Method=POST", 
		"Resource=0", 
		"RecContentType=application/json", 
		"Referer=", 
		"Snapshot=t4.inf", 
		"Mode=HTML", 
		"EncType=application/json", 
		"Body={\"request\":{\"@os\":\"win\",\"@updater\":\"msedgecrx\",\"acceptformat\":\"crx3,download,run,xz,zucc\",\"apps\":[{\"appid\":\"jmjflgjpcpepeafmmgdpfkogkghcpiha\",\"cohort\":\"rrf@0.03\",\"enabled\":true,\"installdate\":7214,\"installedby\":\"other\",\"lang\":\"en-US\",\"ping\":{\"ping_freshness\":\"{1be96855-ffeb-4efb-9dee-c85803ec6761}\",\"rd\":7254},\"targetingattributes\":{\"AppCohort\":\"rrf@0.03\",\"AppMajorVersion\":\"157\",\"AppRollout\":0.03,\"AppVersion\":\"157.0.4341.46\",\""
		"IsInternalUser\":false,\"Priority\":false},\"updatecheck\":{},\"version\":\"1.2.1\"}],\"arch\":\"x64\",\"dedup\":\"cr\",\"domainjoined\":false,\"hw\":{\"avx\":1,\"physmemory\":31,\"sse\":1,\"sse2\":1,\"sse3\":1,\"sse41\":1,\"sse42\":1,\"ssse3\":1},\"ismachine\":1,\"os\":{\"arch\":\"x86_64\",\"deviceformfactor\":\"desktop\",\"platform\":\"Windows\",\"version\":\"10.0.26300.9974\"},\"prodversion\":\"157.0.4341.46\",\"protocol\":\"4.0\",\"requestid\":\"{e3b33ddb-41ad-45d7-b59d-cc616230f09f}\",\""
		"revocationviaomahaenabled\":\"1\",\"sessionid\":\"{059a862d-f671-4130-a799-bf84b3703481}\",\"updaterversion\":\"157.0.4341.46\"}}", 
		LAST);

	web_add_header("X-Microsoft-Update-AppId", 
		"jkgmdjhijhoepbibflgcbedleoefkcej");

	web_add_header("X-Microsoft-Update-Service-Cohort", 
		"1501");

	web_add_header("X-Microsoft-Update-Updater", 
		"msedge-157.0.4341.46");

	web_custom_request("update", 
		"URL=https://edge.microsoft.com/componentupdater/api/v1/update?cup2key=7:zB2NYT-FVgMEjVlIYB0hdqHsuH1yOIrRs-PLMocFZgo&cup2hreq=c3f1cf16f885969e6b21ce11247d5e93c69e8d2787cc963fa843f14e137281f3", 
		"Method=POST", 
		"Resource=0", 
		"RecContentType=application/json", 
		"Referer=", 
		"Snapshot=t5.inf", 
		"Mode=HTML", 
		"EncType=application/json", 
		"Body={\"request\":{\"@os\":\"win\",\"@updater\":\"msedge\",\"acceptformat\":\"crx3,download,run,xz,zucc\",\"apps\":[{\"appid\":\"jkgmdjhijhoepbibflgcbedleoefkcej\",\"brand\":\"EPBR\",\"cached_items\":[{\"sha256\":\"c8156046f8dc4e172a78dd9fc55d25cae57273b13a7cbc953b5faddfd12105c8\"}],\"cohort\":\"rrf@0.69\",\"enabled\":true,\"installdate\":-1,\"lang\":\"en-US\",\"ping\":{\"r\":-2},\"targetingattributes\":{\"AppCohort\":\"rrf@0.69\",\"AppMajorVersion\":\"157\",\"AppRollout\":0.69,\"AppVersion\":\""
		"157.0.4341.46\",\"IsInternalUser\":false,\"Priority\":false,\"Updater\":\"Omaha\",\"UpdaterVersion\":\"1.3.315.17\"},\"updatecheck\":{},\"version\":\"2026.9.18.5\"}],\"arch\":\"x64\",\"dedup\":\"cr\",\"domainjoined\":false,\"hw\":{\"avx\":1,\"physmemory\":31,\"sse\":1,\"sse2\":1,\"sse3\":1,\"sse41\":1,\"sse42\":1,\"ssse3\":1},\"ismachine\":1,\"os\":{\"arch\":\"x86_64\",\"deviceformfactor\":\"desktop\",\"platform\":\"Windows\",\"version\":\"10.0.26300.9974\"},\"prodversion\":\"157.0.4341.46\",\""
		"protocol\":\"4.0\",\"requestid\":\"{7790bf30-41d9-4278-b2df-a3d31ac78a44}\",\"sessionid\":\"{d0f09aa7-d592-4505-a4f2-97ce6a477290}\",\"updaters\":{\"autoupdatecheckenabled\":true,\"ismachine\":1,\"lastchecked\":0,\"laststarted\":0,\"name\":\"Omaha\",\"updatepolicy\":-1,\"version\":\"1.3.315.17\"},\"updaterversion\":\"157.0.4341.46\"}}", 
		LAST);

	web_revert_auto_header("Sec-Mesh-Client-Arch");

	web_revert_auto_header("Sec-Mesh-Client-Edge-Channel");

	web_revert_auto_header("Sec-Mesh-Client-Edge-Version");

	web_revert_auto_header("Sec-Mesh-Client-OS");

	web_revert_auto_header("Sec-Mesh-Client-OS-Version");

	web_revert_auto_header("Sec-Mesh-Client-WebView");

	web_revert_auto_header("X-Microsoft-Update-Interactivity");

	web_add_auto_header("Sec-Fetch-Mode", 
		"navigate");

	web_add_auto_header("Sec-Fetch-Dest", 
		"document");

	web_add_header("Sec-Fetch-User", 
		"?1");

	web_add_header("Upgrade-Insecure-Requests", 
		"1");

	web_add_header("sec-ch-ua", 
		"\"Not-A.Brand\";v=\"99\", \"Microsoft Edge\";v=\"157\", \"Chromium\";v=\"157\"");

	web_add_header("sec-ch-ua-mobile", 
		"?0");

	web_add_header("sec-ch-ua-platform", 
		"\"Windows\"");

	web_add_cookie("ak_bmsc=6482EC7ED1050603ECD2F3D995ACEA0F~000000000000000000000000000000~YAAQD5YqF4BdXcOhAQAAF7MJzQGJgZ7fgGHFkFRRQ67A7kZqcpKOh/TI2Ego4wE8K2vDM2BBEDMj3M9upFw2UO6g8gr2Zkw8w8QbnDC5dTJPDhFLrJVWrAvUyBoDU/nn0yobwOlLVWj5NW8Hm4QWDCsQhQWM3g4x8H6TRUq4E/n5wg58weDIFq1F4S8R1LsQHhW+j5IP7EY4s4duCjFpnFesDU+4giOBCQ1z7YvEXJ736Hd3asR+bn4FC2hnddEGWtIWLJtr5UCEwCV5h5rzBF6492tK4Vesj5kfTzYWyVqcbOKczlKy8DjveDKZkK9tDnIrDE7GIHely3DDwP0WzDwjbeTBUWBVl9Kb/LYhk0fR1Jcf/PbVmOhoR4GGS++VhtFx3Zp7u1YssLI=; DOMAIN="
		"www.tangerine.ca");

	web_add_cookie("AMCV_0AAF22CE52827A080A490D4D%40AdobeOrg=179643557%7CMCIDTS%7C20769%7CvVersion%7C5.5.0; DOMAIN=www.tangerine.ca");

	web_add_cookie("OptanonConsent=isGpcEnabled=0&datestamp=Wed+Nov+11+2026+18%3A56%3A40+GMT-0500+(Eastern+Standard+Time)&version=202502.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&landingPath=https%3A%2F%2Fwww.tangerine.ca%2Fen%2Fpersonal&groups=C0001%3A1%2CC0003%3A1%2CC0002%3A1%2CC0004%3A1; DOMAIN=www.tangerine.ca");

	web_add_cookie("OptanonAlertBoxClosed=2026-11-11T23:57:02.219Z; DOMAIN=www.tangerine.ca");

	web_add_cookie("OptanonConsent=isGpcEnabled=0&datestamp=Wed+Nov+11+2026+18%3A57%3A15+GMT-0500+(Eastern+Standard+Time)&version=202502.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0002%3A1%2CC0004%3A1; DOMAIN=www.tangerine.ca");

	web_add_cookie("kndctr_0AAF22CE52827A080A490D4D_AdobeOrg_cluster=or2; DOMAIN=www.tangerine.ca");

	web_add_cookie("_aid=540615; DOMAIN=www.tangerine.ca");

	web_add_cookie("tng.insights.sessionId=1396df4b-18ef-4632-9804-e2b0f440861323%3BAnonymous; DOMAIN=www.tangerine.ca");

/*Correlation comment - Do not change!  Original value='ip_VisitorCarousel' Name ='interaction-point' Type ='ResponseBased'*/
	web_reg_save_param_regexp(
		"ParamName=interaction-point",
		"RegExp=\\ data-interactionpoint=\"(.*?)\"\\ data-count",
		SEARCH_FILTERS,
		"Scope=Body",
		"IgnoreRedirections=No",
		LAST);

/*Correlation comment - Do not change!  Original value='undefined' Name ='CorrelationParameter' Type ='ResponseBased'*/
	web_reg_save_param_regexp(
		"ParamName=CorrelationParameter",
		"RegExp====\\ '(.*?)'\\)\\ \\{",
		SEARCH_FILTERS,
		"Scope=Body",
		"IgnoreRedirections=No",
		LAST);

	web_url("personal", 
		"URL=https://www.tangerine.ca/en/personal", 
		"Resource=0", 
		"RecContentType=text/html", 
		"Referer=", 
		"Snapshot=t6.inf", 
		"Mode=HTML", 
		EXTRARES, 
		"Url=../evtservvs/?id=", ENDITEM, 
		"Url=../evtservvs/f0y3EAdPxBGIkOUBFfNQPLbjn8j4lyv3_IN1YhTAQ91rwnW_", ENDITEM, 
		"Url=personal/_jcr_content/root/container/container_652395054/container_970270538_/container_686216175/container_copy_1285259141/image.coreimg.svg/1783016528701/plant-pictogram-288x216-cards.svg", ENDITEM, 
		"Url=personal/_jcr_content/root/container/container_652395054/container_970270538_/container_686216175/container_copy_809625414/image.coreimg.svg/1783016528589/wallet-pictogram-288x216-cards.svg", ENDITEM, 
		"Url=personal/_jcr_content/root/container/container_652395054/container_970270538_/container_686216175/container_copy_1396796187/image.coreimg.svg/1783016528564/bar-chart-pictogram-288x216-cards.svg", ENDITEM, 
		"Url=../adobe/dynamicmedia/deliver/dm-aid--32f4470e-3a99-4fed-9dd7-21e7589ca23e/b-hero-592x648.jpg?preferwebp=true&quality=100&width=1280", ENDITEM, 
		"Url=personal/_jcr_content/root/container/container_652395054/container_970270538_/container_686216175/container_copy/image.coreimg.svg/1783016528668/credit-cards-pictogram-288x216-cards.svg", ENDITEM, 
		"Url=personal/_jcr_content/root/container/container_652395054/container_970270538_/container_686216175/container_copy_1834881432/image.coreimg.svg/1783016528553/shield-pictogram-288x216-cards.svg", ENDITEM, 
		"Url=personal/_jcr_content/root/container/container_652395054/container_970270538_/container_686216175/container_copy_272529217/image.coreimg.svg/1783016528542/house-pictogram-288x216-cards.svg", ENDITEM, 
		"Url=personal/_jcr_content/root/container/container_652395054/container_copy_copy_/container_copy/container_456300607_/container_copy_copy__1677949300/container/container/container/container_copy/image.coreimg.svg/1777578560187/icon-plant-pot-light.svg", ENDITEM, 
		"Url=../etc.clientlibs/tangerine/clientlibs/clientlib-onetrust/resources/oneTrust/scripttemplates/202502.1.0/otBannerSdk.js", ENDITEM, 
		"Url=../adobe/dynamicmedia/deliver/dm-aid--d856788c-d552-411f-aef6-42286bb5c473/flipcard-family-mom-baby-playing-drawing-1184x1000-g1437584805.jpg?preferwebp=true&quality=100&width=1280", ENDITEM, 
		"Url=../content/experience-fragments/tangerine/ca/en/search-widget/no-search-results-screen/_jcr_content/root/container/image.coreimg.svg/1744751797042/large-on-light.svg", ENDITEM, 
		"Url=../etc.clientlibs/tangerine/clientlibs/clientlib-onetrust/resources/oneTrust/scripttemplates/202502.1.0/assets/otCommonStyles.css", ENDITEM, 
		"Url=../etc.clientlibs/tangerine/clientlibs/clientlib-onetrust/resources/oneTrust/consent/abe5e4e6-b00b-4dc8-aa66-ea460fe6a634/0195aa99-ba4d-7be7-a2d8-6fae40dd9ed4/logos/static/ot_close.svg", ENDITEM, 
		"Url=../etc.clientlibs/tangerine/clientlibs/clientlib-onetrust/resources/oneTrust/consent/abe5e4e6-b00b-4dc8-aa66-ea460fe6a634/0195aa99-ba4d-7be7-a2d8-6fae40dd9ed4/logos/static/ot_guard_logo.svg", ENDITEM, 
		"Url=../etc.clientlibs/tangerine/clientlibs/clientlib-onetrust/resources/oneTrust/consent/abe5e4e6-b00b-4dc8-aa66-ea460fe6a634/0195aa99-ba4d-7be7-a2d8-6fae40dd9ed4/logos/static/ot_company_logo.png", ENDITEM, 
		"Url=../etc.clientlibs/tangerine/clientlibs/clientlib-onetrust/resources/oneTrust/consent/abe5e4e6-b00b-4dc8-aa66-ea460fe6a634/0195aa99-ba4d-7be7-a2d8-6fae40dd9ed4/logos/static/powered_by_logo.svg", ENDITEM, 
		"Url=../adobe/dynamicmedia/deliver/dm-aid--4bd8d007-f6e0-489b-8c03-d037be8e051d/qrcode-lg-md-1x1-contain-darkmode-en.png?preferwebp=true&quality=100&width=1280", ENDITEM, 
		"Url=../adobe/dynamicmedia/deliver/dm-aid--ea50b12c-3b65-4e39-b8a7-7fe778ab0c7c/jdp-homepage-1280x640-en.jpg?preferwebp=true&quality=100&width=1280", ENDITEM, 
		"Url=../adobe/dynamicmedia/deliver/dm-aid--50b69abc-9109-4938-9f97-7985ce6e8eb6/line-chart-phone-digital-wealth-platform-592x488-mockup-darkgray-en.png?preferwebp=true&quality=100&width=1280", ENDITEM, 
		"Url=../adobe/dynamicmedia/deliver/dm-aid--d66546d1-1a53-452e-ae8b-b7a8fd6d6222/2026-forbes-wbbanks-1280x640-en.jpg?preferwebp=true&quality=100&width=1280", ENDITEM, 
		"Url=../adobe/dynamicmedia/deliver/dm-aid--f562bf2b-c0f4-464a-abd6-913382c961d8/father-boy-playing-sunset-flying-1872x2049-1532870985.jpg?preferwebp=true&quality=100&width=1280", ENDITEM, 
		"Url=../content/experience-fragments/tangerine/ca/en/mfz/join-our-app/join-our-app-homepage/_jcr_content/root/container_copy/container/container_copy_copy_/container_copy_copy_1822156692/image.coreimg.svg/1762368888976/icon-app-rating.svg", ENDITEM, 
		"Url=../content/experience-fragments/tangerine/ca/en/footer/master/_jcr_content/root/container/container_1741627176/container/container/image.coreimg.svg/1705966281243/ios-app-store.svg", ENDITEM, 
		"Url=../content/experience-fragments/tangerine/ca/en/footer/master/_jcr_content/root/container/container_1741627176/container/container/image_1128814434.coreimg.svg/1705966313154/android-app-store.svg", ENDITEM, 
		"Url=../content/experience-fragments/tangerine/ca/en/footer/master/_jcr_content/root/container/container_1741627176/container_1851780169/container_1385568956/image_copy.coreimg.svg/1705966107286/instagram.svg", ENDITEM, 
		"Url=../content/experience-fragments/tangerine/ca/en/footer/master/_jcr_content/root/container/container_1741627176/container_1851780169/container_1385568956/image_copy_copy_2029043166.coreimg.svg/1705966135363/linkedin.svg", ENDITEM, 
		"Url=../adobe/dynamicmedia/deliver/dm-aid--edd5b24f-23ab-4dd9-a313-bdc9859ab31b/app-rating-qrcode.png?preferwebp=true&quality=100&width=1280", ENDITEM, 
		"Url=../content/experience-fragments/tangerine/ca/en/footer/master/_jcr_content/root/container/container_1741627176/container_1851780169/container_1385568956/image_copy_copy_669594526.coreimg.svg/1705966161829/twitter.svg", ENDITEM, 
		"Url=../content/experience-fragments/tangerine/ca/en/footer/master/_jcr_content/root/container/container_1741627176/container_1851780169/container_1385568956/image_copy_copy_1655502265.coreimg.svg/1705966145167/youtube.svg", ENDITEM, 
		"Url=../content/experience-fragments/tangerine/ca/en/footer/master/_jcr_content/root/container/container_1741627176/container_1851780169/container_1385568956/image_copy_copy_1371551471.coreimg.svg/1706952713591/tiktok.svg", ENDITEM, 
		"Url=../content/experience-fragments/tangerine/ca/en/footer/master/_jcr_content/root/container/container_1741627176/container_1851780169/container_1385568956/image_copy_copy_1340051228.coreimg.svg/1705966171796/facebook.svg", ENDITEM, 
		"Url=../content/experience-fragments/tangerine/ca/en/footer/master/_jcr_content/root/container/container_1741627176/container_1394683010/image.coreimg.svg/1729613140581/cdic-digital-symbol.svg", ENDITEM, 
		"Url=../content/experience-fragments/tangerine/ca/en/mfz/your-wealth-snapshot/your-wealth-snapshot-homepage/_jcr_content/root/container_copy_copy/container/container_copy_copy_/container_copy_copy_/image.coreimg.svg/1762369057931/icon-app-rating-alt.svg", ENDITEM, 
		"Url=personal/_jcr_content/root/container/container_652395054/container_copy_copy_/container_copy/container_456300607_/container_copy_copy__522782145/container/container/container/container_copy_copy/image.coreimg.svg/1777578597323/wallet-light.svg", ENDITEM, 
		"Url=../adobe/dynamicmedia/deliver/dm-aid--e050ec3a-0164-4836-b246-ff34d8a85b93/flipcard-elite-world-credit-card-1184x1000-orange-en.jpg?preferwebp=true&quality=100&width=1280", ENDITEM, 
		LAST);

	web_add_auto_header("Sec-Fetch-Dest", 
		"empty");

	web_add_auto_header("Sec-Fetch-Mode", 
		"no-cors");

	web_add_header("Sec-Fetch-Storage-Access", 
		"active");

	web_add_header("X-ECS-Client-Last-Telemetry-Events", 
		"ecs_client_library_name=IntuneDesktopMAM,ecs_client_app_name=com.microsoft.edge,ecs_client_version=2.4.2.0");

	web_url("1.0_2", 
		"URL=https://config.edge.skype.com/config/v1/Intune/1.0?agents=CLI_DesktopMAM&appId=com.microsoft.edge&appVersion=157.0.4341.46&clientId=8fcda4f9-0248-46ea-8edc-3d78ced6a6f5&cloud=Public&osType=windows&osVersion_version=10.0.26300.9974&tenantId=de08c407-19b9-427d-9fe8-edf254300ca7", 
		"Resource=0", 
		"RecContentType=application/json", 
		"Referer=", 
		"Snapshot=t7.inf", 
		"Mode=HTML", 
		LAST);

	web_add_header("Sec-Mesh-Client-Arch", 
		"x86_64");

	web_add_header("Sec-Mesh-Client-Edge-Channel", 
		"stable");

	web_add_header("Sec-Mesh-Client-Edge-Version", 
		"157.0.4341.46");

	web_add_header("Sec-Mesh-Client-OS", 
		"Windows");

	web_add_header("Sec-Mesh-Client-OS-Version", 
		"10.0.26300");

	web_add_header("Sec-Mesh-Client-WebView", 
		"0");

	web_add_header("X-Microsoft-Update-AppId", 
		"nmcnjaceoejcjmmnabjnmfpoanaengif");

	web_add_header("X-Microsoft-Update-Interactivity", 
		"bg");

	web_add_header("X-Microsoft-Update-Service-Cohort", 
		"9242");

	web_add_header("X-Microsoft-Update-Updater", 
		"msedge-157.0.4341.46");

	web_custom_request("update_2", 
		"URL=https://edge.microsoft.com/componentupdater/api/v1/update?cup2key=7:OhGSCSRLx5tRNMC-fTirCihy0og8rWFQgvoIVAV0_eA&cup2hreq=ece45d05829f102995a4a59cf7b2cf697e943b5f26502139a9d9ffad67751197", 
		"Method=POST", 
		"Resource=0", 
		"RecContentType=application/json", 
		"Referer=", 
		"Snapshot=t8.inf", 
		"Mode=HTML", 
		"EncType=application/json", 
		"Body={\"request\":{\"@os\":\"win\",\"@updater\":\"msedge\",\"acceptformat\":\"crx3,download,run,xz,zucc\",\"apps\":[{\"appid\":\"nmcnjaceoejcjmmnabjnmfpoanaengif\",\"brand\":\"EPBR\",\"cached_items\":[{\"sha256\":\"a9592ae40712c6cfdf7d142e2563ca4ec8f696cfe53e267ad0ea630c43beaa33\"}],\"cohort\":\"rrf@0.08\",\"enabled\":true,\"installdate\":-1,\"lang\":\"en-US\",\"ping\":{\"r\":-2},\"targetingattributes\":{\"AppCohort\":\"rrf@0.08\",\"AppMajorVersion\":\"157\",\"AppRollout\":0.08,\"AppVersion\":\""
		"157.0.4341.46\",\"IsInternalUser\":false,\"Priority\":false,\"Updater\":\"Omaha\",\"UpdaterVersion\":\"1.3.315.17\"},\"updatecheck\":{},\"version\":\"2026.1.30.1\"}],\"arch\":\"x64\",\"dedup\":\"cr\",\"domainjoined\":false,\"hw\":{\"avx\":1,\"physmemory\":31,\"sse\":1,\"sse2\":1,\"sse3\":1,\"sse41\":1,\"sse42\":1,\"ssse3\":1},\"ismachine\":1,\"os\":{\"arch\":\"x86_64\",\"deviceformfactor\":\"desktop\",\"platform\":\"Windows\",\"version\":\"10.0.26300.9974\"},\"prodversion\":\"157.0.4341.46\",\""
		"protocol\":\"4.0\",\"requestid\":\"{9f0b1139-e5ee-4293-96bb-68cfbf74ed24}\",\"sessionid\":\"{8419367d-2bcd-4230-a74b-18bdb95b0f34}\",\"updaters\":{\"autoupdatecheckenabled\":true,\"ismachine\":1,\"lastchecked\":0,\"laststarted\":0,\"name\":\"Omaha\",\"updatepolicy\":-1,\"version\":\"1.3.315.17\"},\"updaterversion\":\"157.0.4341.46\"}}", 
		LAST);

	web_add_auto_header("Sec-Fetch-Mode", 
		"cors");

	web_add_cookie("ak_bmsc=6482EC7ED1050603ECD2F3D995ACEA0F~000000000000000000000000000000~YAAQD5YqF0hnXcOhAQAAANcJzQEAjgxF09BkLFXXMxhDH4hBuTLNBvaBWm9n0ZEXRNwkz3PF0sRB+/3sAEwjvrd0le4QhtKLPJWG8tTkaZ0EI8Jk4uycYd7hbgZ3JzxD0bB5gxBHSHpeXz4YG+2m1bBzUZtwynMwTZ5G4/YbOD+acmVI5e2rlzOAuVK+ppi6AafWOFf6Ce2FPFjGJTcv+TKPyTztNFqPh/kW168vH2jqxlMlULuDE+jH88CDm2tWjJH7QSlIcyf1+0GalQv21riExjHPutKO5uCyBOk6ZY13A51ntlJHi96CDp4Au3YViPtFe/qj/9jaPeGt3qjJNZ++AN+lLXMVBMgAqM2iCSyeD9oW28qHJ/7jDzGD1obpxIUd+ogk8qLOXFNJO164Gtl1pk4ActXfTq"
		"/x; DOMAIN=www.tangerine.ca");

	web_add_auto_header("Sec-Fetch-Site", 
		"same-origin");

	web_add_header("sec-ch-ua", 
		"\"Not-A.Brand\";v=\"99\", \"Microsoft Edge\";v=\"157\", \"Chromium\";v=\"157\"");

	web_add_header("sec-ch-ua-mobile", 
		"?0");

	web_add_header("sec-ch-ua-platform", 
		"\"Windows\"");

	lr_think_time(4);

/*Correlation comment - Do not change!  Original value='6482EC7ED1050603ECD2F3D995ACEA0F~000000000000000000000000000000~YAAQD5YqFwdsXcOhAQAA3ugJzQEIYQ5xB5B7e5nOFkEeaPLELt4Wjd41xsPUKy7sj4ZsSYH4CYZWIHxLDkHepmweGfUI8WFiFGKOUOoBuMEN1jzRv5tFczs1cnnnsc7bPDKTF1egDweE34KDjvennjeCyaM3NxgTGC8z9EfrrM4q1kCEubM536sSLuRf8CFCl167shvEsP/QvxnIbtCnz4Nj/nnHYOPuKP5G7dvVvbNP+Fj4xvYUlErwLC/TS36TB44U8YaEywJT5TfqlQgTxo6yI6TgBwIsb6GVm0u8yhgPuZO8tyi+xFWa0v9jF3f5H7b+JumvPCwyOUCewdYodMPAywfs0BR7lpIlTqddoDedd0RWBG2WHXDEVUvF4iSiPgNrPaXZUai08Slc9hUocwkHrvWNaJkSrcKQ' Name ='ak_bmsc' Type ='ResponseBased'*/
	web_reg_save_param_regexp(
		"ParamName=ak_bmsc",
		"RegExp=ak_bmsc=(.*?);",
		SEARCH_FILTERS,
		"Scope=Cookies",
		"IgnoreRedirections=No",
		"RequestUrl=*/icon-chevron-right-light.svg*",
		LAST);

	web_url("abe5e4e6-b00b-4dc8-aa66-ea460fe6a634.json", 
		"URL=https://www.tangerine.ca/etc.clientlibs/tangerine/clientlibs/clientlib-onetrust/resources/oneTrust/consent/abe5e4e6-b00b-4dc8-aa66-ea460fe6a634/abe5e4e6-b00b-4dc8-aa66-ea460fe6a634.json", 
		"Resource=0", 
		"RecContentType=application/json", 
		"Referer=https://www.tangerine.ca/en/personal", 
		"Snapshot=t9.inf", 
		"Mode=HTML", 
		EXTRARES, 
		"Url=/content/dam/tangerine-shared/icons/icon-search-light.svg", "Referer=https://www.tangerine.ca/etc.clientlibs/tangerine/clientlibs/clientlib-search.lc-5f5ad8d75d34345c8467829dac512147-lc.min.css", ENDITEM, 
		"Url=/content/dam/tangerine-shared/icons/icon-close-light.svg", "Referer=https://www.tangerine.ca/etc.clientlibs/tangerine/clientlibs/clientlib-site.lc-548a3a3dd9416446a4c03659772d3bef-lc.min.css", ENDITEM, 
		"Url=/content/dam/tangerine-shared/icons/icon-chevron-right-light.svg", "Referer=https://www.tangerine.ca/etc.clientlibs/tangerine/clientlibs/clientlib-site.lc-548a3a3dd9416446a4c03659772d3bef-lc.min.css", ENDITEM, 
		"Url=/content/dam/tangerine-shared/icons/icon-arrow-left-light.svg", "Referer=https://www.tangerine.ca/etc.clientlibs/tangerine/clientlibs/clientlib-site.lc-548a3a3dd9416446a4c03659772d3bef-lc.min.css", ENDITEM, 
		"Url=/content/dam/tangerine-shared/icons/icon-stars-light.svg", "Referer=https://www.tangerine.ca/etc.clientlibs/tangerine/clientlibs/clientlib-site.lc-548a3a3dd9416446a4c03659772d3bef-lc.min.css", ENDITEM, 
		"Url=/content/dam/tangerine-shared/icons/icon-location-light.svg", "Referer=https://www.tangerine.ca/etc.clientlibs/tangerine/clientlibs/clientlib-site.lc-548a3a3dd9416446a4c03659772d3bef-lc.min.css", ENDITEM, 
		"Url=/content/dam/tangerine-shared/icons/icon-language-light.svg", "Referer=https://www.tangerine.ca/etc.clientlibs/tangerine/clientlibs/clientlib-site.lc-548a3a3dd9416446a4c03659772d3bef-lc.min.css", ENDITEM, 
		"Url=/content/dam/tangerine-shared/icons/icon-help-light.svg", "Referer=https://www.tangerine.ca/etc.clientlibs/tangerine/clientlibs/clientlib-site.lc-548a3a3dd9416446a4c03659772d3bef-lc.min.css", ENDITEM, 
		LAST);

	web_add_auto_header("Sec-Fetch-Site", 
		"none");

	web_add_auto_header("Sec-Fetch-Mode", 
		"no-cors");

	web_add_header("Sec-Mesh-Client-Arch", 
		"x86_64");

	web_add_header("Sec-Mesh-Client-Edge-Channel", 
		"stable");

	web_add_header("Sec-Mesh-Client-Edge-Version", 
		"157.0.4341.46");

	web_add_header("Sec-Mesh-Client-OS", 
		"Windows");

	web_add_header("Sec-Mesh-Client-OS-Version", 
		"10.0.26300");

	web_add_header("Sec-Mesh-Client-WebView", 
		"0");

	web_add_header("X-Microsoft-Update-AppId", 
		"jkgmdjhijhoepbibflgcbedleoefkcej,fppmbhmldokgmleojlplaaodlkibgikh,fgbafbciocncjfbbonhocjaohoknlaco,ndikpojcjlepofdkaaldkinkjbeeebkl,laoigpblnllgcgjnjnllmfolckpjlhki,alpjnmnfbgfkmmpcfpejmmoebdndedno,ojblfafjmiikbkepnnolpgbbhejhlcim,pghocgajpebopihickglahgebcmkcekh,kpfehajjjbbcifeehjgfgnabifknmdad,mpicjakjneaggahlnmbojhjpnileolnb,eeobbhfgfagbclfofmgbdfoicabjdbkn,ahmaebgpfccdhgidjaidaoojjcijckba,oankkpibpaokgecfckkdkgaoafllipag,ohckeflnhegojcjlcpbfpciadgikcohk,llmidpclgepbgbgoecnhcmgfhmfplfao,"
		"gllimckfbolmioaaihpppacjccghejen,jbfaflocpnkhbgcijpkiafdpbjkedane,kmkacjgmmfchkbeglfbjjeidfckbnkca,plbmmhnabegcabfbcejohgjpkamkddhn,eodcfhpdifcaamjndfbdfbbhjkjgbion,ohjmcpfnpmlgfkommepbhamjmanldlae,kieecehchjjaaepgajdhcehijkehdenm,jpinkpebmplndiafioikiciobeafamld,jcmcegpcehdchljeldgmmfbgcpnmgedo,npbipokbgmclmkjhfjicdgnedhkocjpl,fmbfidpnnknmblionmcahabilfoageoe,eiihffpgcdgabdmcecnakaohbclgfbmb,lfmeghnikdkbonehgjihjebgioakijgn,pbdgbpmpeenomngainidcjmopnklimmf,lkkdlcloifjinapabfonaibjijloebfb");

	web_add_header("X-Microsoft-Update-Interactivity", 
		"bg");

	web_add_header("X-Microsoft-Update-Service-Cohort", 
		"7344");

	web_add_header("X-Microsoft-Update-Updater", 
		"msedge-157.0.4341.46");

	web_custom_request("update_3", 
		"URL=https://edge.microsoft.com/componentupdater/api/v1/update?cup2key=7:Z2XNhaLJGBUaErR1MG1jh5h6I8dWbci3FA5L671nfrY&cup2hreq=5580c0af927c6dd98fe25d28673ee917f466b2a27c524b2bb9cdca0e054fc57b", 
		"Method=POST", 
		"Resource=0", 
		"RecContentType=application/json", 
		"Referer=", 
		"Snapshot=t10.inf", 
		"Mode=HTML", 
		"EncType=application/json", 
		"Body={\"request\":{\"@os\":\"win\",\"@updater\":\"msedge\",\"acceptformat\":\"crx3,download,run,xz,zucc\",\"apps\":[{\"appid\":\"jkgmdjhijhoepbibflgcbedleoefkcej\",\"brand\":\"EPBR\",\"cached_items\":[{\"sha256\":\"c8156046f8dc4e172a78dd9fc55d25cae57273b13a7cbc953b5faddfd12105c8\"}],\"cohort\":\"rrf@0.86\",\"enabled\":true,\"installdate\":-1,\"lang\":\"en-US\",\"ping\":{\"r\":-2},\"targetingattributes\":{\"AppCohort\":\"rrf@0.86\",\"AppMajorVersion\":\"157\",\"AppRollout\":0.86,\"AppVersion\":\""
		"157.0.4341.46\",\"IsInternalUser\":false,\"Priority\":false,\"Updater\":\"Omaha\",\"UpdaterVersion\":\"1.3.315.17\"},\"updatecheck\":{},\"version\":\"2026.9.18.5\"},{\"appid\":\"fppmbhmldokgmleojlplaaodlkibgikh\",\"brand\":\"EPBR\",\"cached_items\":[{\"sha256\":\"a81d1959892ae4180554347df1b97834abba2e1a5e6b9aeba000ecea26eabecc\"}],\"cohort\":\"rrf@0.02\",\"enabled\":true,\"installdate\":-1,\"lang\":\"en-US\",\"ping\":{\"r\":-2},\"targetingattributes\":{\"AppCohort\":\"rrf@0.02\",\"AppMajorVersion"
		"\":\"157\",\"AppRollout\":0.02,\"AppVersion\":\"157.0.4341.46\",\"IsInternalUser\":false,\"Priority\":false,\"Updater\":\"Omaha\",\"UpdaterVersion\":\"1.3.315.17\"},\"updatecheck\":{},\"version\":\"1.15.0.1\"},{\"appid\":\"fgbafbciocncjfbbonhocjaohoknlaco\",\"brand\":\"EPBR\",\"cached_items\":[{\"sha256\":\"d3280a2d97d1bd59dd97decf1728960096362a103cab0a770e9201be9a61737d\"}],\"cohort\":\"rrf@0.04\",\"enabled\":true,\"installdate\":-1,\"lang\":\"en-US\",\"ping\":{\"r\":-2},\"targetingattributes\":"
		"{\"AppCohort\":\"rrf@0.04\",\"AppMajorVersion\":\"157\",\"AppRollout\":0.04,\"AppVersion\":\"157.0.4341.46\",\"IsInternalUser\":false,\"Priority\":false,\"Updater\":\"Omaha\",\"UpdaterVersion\":\"1.3.315.17\"},\"updatecheck\":{},\"version\":\"2026.10.12.1\"},{\"appid\":\"ndikpojcjlepofdkaaldkinkjbeeebkl\",\"brand\":\"EPBR\",\"cached_items\":[{\"sha256\":\"720517793663c90e0dbd77cb42709bac49af733f83f73320ba89859d9b0310e0\"}],\"cohort\":\"rrf@0.58\",\"enabled\":true,\"installdate\":-1,\"lang\":\""
		"en-US\",\"ping\":{\"r\":-2},\"targetingattributes\":{\"AppCohort\":\"rrf@0.58\",\"AppMajorVersion\":\"157\",\"AppRollout\":0.58,\"AppVersion\":\"157.0.4341.46\",\"IsInternalUser\":false,\"Priority\":false,\"Updater\":\"Omaha\",\"UpdaterVersion\":\"1.3.315.17\"},\"updatecheck\":{},\"version\":\"10.34.0.84\"},{\"appid\":\"laoigpblnllgcgjnjnllmfolckpjlhki\",\"brand\":\"EPBR\",\"cohort\":\"rrf@0.63\",\"enabled\":true,\"installdate\":-1,\"lang\":\"en-US\",\"ping\":{\"r\":-2},\"targetingattributes\":{\""
		"AppCohort\":\"rrf@0.63\",\"AppMajorVersion\":\"157\",\"AppRollout\":0.63,\"AppVersion\":\"157.0.4341.46\",\"IsInternalUser\":false,\"Priority\":false,\"Updater\":\"Omaha\",\"UpdaterVersion\":\"1.3.315.17\"},\"updatecheck\":{},\"version\":\"1.0.7.1652906823\"},{\"appid\":\"alpjnmnfbgfkmmpcfpejmmoebdndedno\",\"brand\":\"EPBR\",\"cached_items\":[{\"sha256\":\"cc291515e29b5f87753441b3c36cbbc78bbddd8d4af016eb522b221068adb430\"}],\"cohort\":\"rrf@0.55\",\"enabled\":true,\"installdate\":-1,\"lang\":\""
		"en-US\",\"ping\":{\"r\":-2},\"targetingattributes\":{\"AppCohort\":\"rrf@0.55\",\"AppMajorVersion\":\"157\",\"AppRollout\":0.55,\"AppVersion\":\"157.0.4341.46\",\"IsInternalUser\":false,\"Priority\":false,\"Updater\":\"Omaha\",\"UpdaterVersion\":\"1.3.315.17\"},\"updatecheck\":{},\"version\":\"73.0.0.0\"},{\"appid\":\"ojblfafjmiikbkepnnolpgbbhejhlcim\",\"brand\":\"EPBR\",\"cached_items\":[{\"sha256\":\"4906bd7a9eefe3a91738213e016c47e334882047cd6236f97267ccf589e701af\"}],\"cohort\":\"rrf@0.73\",\""
		"enabled\":true,\"installdate\":-1,\"lang\":\"en-US\",\"ping\":{\"r\":-2},\"targetingattributes\":{\"AppCohort\":\"rrf@0.73\",\"AppMajorVersion\":\"157\",\"AppRollout\":0.73,\"AppVersion\":\"157.0.4341.46\",\"IsInternalUser\":false,\"Priority\":false,\"Updater\":\"Omaha\",\"UpdaterVersion\":\"1.3.315.17\"},\"updatecheck\":{},\"version\":\"4.10.3112.0\"},{\"appid\":\"pghocgajpebopihickglahgebcmkcekh\",\"brand\":\"EPBR\",\"cached_items\":[{\"sha256\":\""
		"4f1384fbf5a9924759a947c162f80edcd91446146f48ac2320c31c1c2b6d7fe2\"}],\"cohort\":\"rrf@1.00\",\"enabled\":true,\"installdate\":-1,\"lang\":\"en-US\",\"ping\":{\"r\":-2},\"targetingattributes\":{\"AppCohort\":\"rrf@1.00\",\"AppMajorVersion\":\"157\",\"AppRollout\":1,\"AppVersion\":\"157.0.4341.46\",\"IsInternalUser\":false,\"Priority\":false,\"Updater\":\"Omaha\",\"UpdaterVersion\":\"1.3.315.17\"},\"updatecheck\":{},\"version\":\"3.0.0.20\"},{\"appid\":\"kpfehajjjbbcifeehjgfgnabifknmdad\",\"brand\""
		":\"EPBR\",\"cached_items\":[{\"sha256\":\"00af3f07b5abb71f6d30337e1eef62fa280f06ef19485c0cf6b72171f92ccc0a\"}],\"cohort\":\"rrf@0.16\",\"enabled\":true,\"installdate\":-1,\"lang\":\"en-US\",\"ping\":{\"r\":-2},\"targetingattributes\":{\"AppCohort\":\"rrf@0.16\",\"AppMajorVersion\":\"157\",\"AppRollout\":0.16,\"AppVersion\":\"157.0.4341.46\",\"IsInternalUser\":false,\"Priority\":false,\"Updater\":\"Omaha\",\"UpdaterVersion\":\"1.3.315.17\"},\"updatecheck\":{},\"version\":\"120.0.6050.0\"},{\"appid"
		"\":\"mpicjakjneaggahlnmbojhjpnileolnb\",\"brand\":\"EPBR\",\"cached_items\":[{\"sha256\":\"96b9640eef0668f4d266932438731ee473f9c1186e1c64440512025567be62b7\"}],\"cohort\":\"rrf@0.66\",\"enabled\":true,\"installdate\":-1,\"lang\":\"en-US\",\"ping\":{\"r\":-2},\"targetingattributes\":{\"AppCohort\":\"rrf@0.66\",\"AppMajorVersion\":\"157\",\"AppRollout\":0.66,\"AppVersion\":\"157.0.4341.46\",\"IsInternalUser\":false,\"Priority\":false,\"Updater\":\"Omaha\",\"UpdaterVersion\":\"1.3.315.17\"},\""
		"updatecheck\":{},\"version\":\"4.0.1.32\"},{\"appid\":\"eeobbhfgfagbclfofmgbdfoicabjdbkn\",\"brand\":\"EPBR\",\"cached_items\":[{\"sha256\":\"cde4f808f038aaffece9680c0356ded00c81c4559e0a431acb45d1276425d9eb\"}],\"cohort\":\"rrf@0.94\",\"enabled\":true,\"installdate\":-1,\"lang\":\"en-US\",\"ping\":{\"r\":-2},\"targetingattributes\":{\"AppCohort\":\"rrf@0.94\",\"AppMajorVersion\":\"157\",\"AppRollout\":0.94,\"AppVersion\":\"157.0.4341.46\",\"IsInternalUser\":false,\"Priority\":false,\"Updater\":\""
		"Omaha\",\"UpdaterVersion\":\"1.3.315.17\"},\"updatecheck\":{},\"version\":\"1.0.0.12\"},{\"appid\":\"ahmaebgpfccdhgidjaidaoojjcijckba\",\"brand\":\"EPBR\",\"cached_items\":[{\"sha256\":\"07e0ad6da3d30a27962c6e09da9798ba1745856eaad71a036e2f639e93ea0b27\"}],\"cohort\":\"rrf@0.29\",\"enabled\":true,\"installdate\":-1,\"lang\":\"en-US\",\"ping\":{\"r\":-2},\"targetingattributes\":{\"AppCohort\":\"rrf@0.29\",\"AppMajorVersion\":\"157\",\"AppRollout\":0.29,\"AppVersion\":\"157.0.4341.46\",\""
		"IsInternalUser\":false,\"Priority\":false,\"Updater\":\"Omaha\",\"UpdaterVersion\":\"1.3.315.17\"},\"updatecheck\":{},\"version\":\"3.2.0.0\"},{\"appid\":\"oankkpibpaokgecfckkdkgaoafllipag\",\"brand\":\"EPBR\",\"cached_items\":[{\"sha256\":\"0f1ccded57bb4b5edc565cb3e8ec03b9f164b400ca2a9b446f2b52da790a1804\"}],\"cohort\":\"rrf@0.12\",\"enabled\":true,\"installdate\":-1,\"lang\":\"en-US\",\"ping\":{\"r\":-2},\"targetingattributes\":{\"AppCohort\":\"rrf@0.12\",\"AppMajorVersion\":\"157\",\""
		"AppRollout\":0.12,\"AppVersion\":\"157.0.4341.46\",\"IsInternalUser\":false,\"Priority\":false,\"Updater\":\"Omaha\",\"UpdaterVersion\":\"1.3.315.17\"},\"updatecheck\":{},\"version\":\"6498.2026.10.20\"},{\"appid\":\"ohckeflnhegojcjlcpbfpciadgikcohk\",\"brand\":\"EPBR\",\"cached_items\":[{\"sha256\":\"95fd9d48e4fc245a3f3a99a3a16ecd1355050ba3f4afc555f19a97c7f9b49677\"}],\"cohort\":\"rrf@0.77\",\"enabled\":true,\"installdate\":-1,\"lang\":\"en-US\",\"ping\":{\"r\":-2},\"targetingattributes\":{\""
		"AppCohort\":\"rrf@0.77\",\"AppMajorVersion\":\"157\",\"AppRollout\":0.77,\"AppVersion\":\"157.0.4341.46\",\"IsInternalUser\":false,\"Priority\":false,\"Updater\":\"Omaha\",\"UpdaterVersion\":\"1.3.315.17\"},\"updatecheck\":{},\"version\":\"0.0.1.7\"},{\"appid\":\"llmidpclgepbgbgoecnhcmgfhmfplfao\",\"brand\":\"EPBR\",\"cached_items\":[{\"sha256\":\"d79b0a389269f7011191a4f5f17a27919b6d43f34363919296e67e6c0107a6fd\"}],\"cohort\":\"rrf@0.20\",\"enabled\":true,\"installdate\":-1,\"lang\":\"en-US\",\""
		"ping\":{\"r\":-2},\"targetingattributes\":{\"AppCohort\":\"rrf@0.20\",\"AppMajorVersion\":\"157\",\"AppRollout\":0.2,\"AppVersion\":\"157.0.4341.46\",\"IsInternalUser\":false,\"Priority\":false,\"Updater\":\"Omaha\",\"UpdaterVersion\":\"1.3.315.17\"},\"updatecheck\":{},\"version\":\"2.1.114.0\"},{\"appid\":\"gllimckfbolmioaaihpppacjccghejen\",\"brand\":\"EPBR\",\"cached_items\":[{\"sha256\":\"8d3db5ddf4bd3cfca1863869fc72b1d7365604f046a8bd90518f5a40716d1da9\"}],\"cohort\":\"rrf@0.01\",\"enabled\""
		":true,\"installdate\":-1,\"lang\":\"en-US\",\"ping\":{\"r\":-2},\"targetingattributes\":{\"AppCohort\":\"rrf@0.01\",\"AppMajorVersion\":\"157\",\"AppRollout\":0.01,\"AppVersion\":\"157.0.4341.46\",\"IsInternalUser\":false,\"Priority\":false,\"Updater\":\"Omaha\",\"UpdaterVersion\":\"1.3.315.17\"},\"updatecheck\":{},\"version\":\"1.2.0.3\"},{\"appid\":\"jbfaflocpnkhbgcijpkiafdpbjkedane\",\"brand\":\"EPBR\",\"cached_items\":[{\"sha256\":\""
		"38448ae7d29b58eea0215abd590ba55279c08a4450469b706a0307866502d53a\"}],\"cohort\":\"rrf@0.05\",\"enabled\":true,\"installdate\":-1,\"lang\":\"en-US\",\"ping\":{\"r\":-2},\"targetingattributes\":{\"AppCohort\":\"rrf@0.05\",\"AppMajorVersion\":\"157\",\"AppRollout\":0.05,\"AppVersion\":\"157.0.4341.46\",\"IsInternalUser\":false,\"Priority\":false,\"Updater\":\"Omaha\",\"UpdaterVersion\":\"1.3.315.17\"},\"updatecheck\":{},\"version\":\"1.0.0.38\"},{\"appid\":\"kmkacjgmmfchkbeglfbjjeidfckbnkca\",\""
		"brand\":\"EPBR\",\"cached_items\":[{\"sha256\":\"e51d3f4ef39e9104ec54e50dda09696dc25e190990c201a202292cc0ce740397\"}],\"cohort\":\"rrf@0.82\",\"enabled\":true,\"installdate\":-1,\"lang\":\"en-US\",\"ping\":{\"r\":-2},\"targetingattributes\":{\"AppCohort\":\"rrf@0.82\",\"AppMajorVersion\":\"157\",\"AppRollout\":0.82,\"AppVersion\":\"157.0.4341.46\",\"IsInternalUser\":false,\"Priority\":false,\"Updater\":\"Omaha\",\"UpdaterVersion\":\"1.3.315.17\"},\"updatecheck\":{},\"version\":\"2026.6.5.1\"},{\""
		"appid\":\"plbmmhnabegcabfbcejohgjpkamkddhn\",\"brand\":\"EPBR\",\"cached_items\":[{\"sha256\":\"1e1174204f8a0a13de2e224a1be882d2724a6fd13ba18a895fd5098fd5552460\"}],\"cohort\":\"rrf@0.08\",\"enabled\":true,\"installdate\":-1,\"lang\":\"en-US\",\"ping\":{\"r\":-2},\"targetingattributes\":{\"AppCohort\":\"rrf@0.08\",\"AppMajorVersion\":\"157\",\"AppRollout\":0.08,\"AppVersion\":\"157.0.4341.46\",\"IsInternalUser\":false,\"Priority\":false,\"Updater\":\"Omaha\",\"UpdaterVersion\":\"1.3.315.17\"},\""
		"updatecheck\":{},\"version\":\"3057\"},{\"appid\":\"eodcfhpdifcaamjndfbdfbbhjkjgbion\",\"brand\":\"EPBR\",\"cached_items\":[{\"sha256\":\"df5bb9f2afeb58b7c813d43eaa32cf6b240e346614ec52425bb5ff323450cd51\"}],\"cohort\":\"rrf@0.57\",\"enabled\":true,\"installdate\":-1,\"lang\":\"en-US\",\"ping\":{\"r\":-2},\"targetingattributes\":{\"AppCohort\":\"rrf@0.57\",\"AppMajorVersion\":\"157\",\"AppRollout\":0.57,\"AppVersion\":\"157.0.4341.46\",\"IsInternalUser\":false,\"Priority\":false,\"Updater\":\""
		"Omaha\",\"UpdaterVersion\":\"1.3.315.17\"},\"updatecheck\":{},\"version\":\"2026.5.28.1\"},{\"appid\":\"ohjmcpfnpmlgfkommepbhamjmanldlae\",\"brand\":\"EPBR\",\"cached_items\":[{\"sha256\":\"77ab8c118fd534ab1cf48f984963d6d35ebf06580b0041ec7d594ce88561ad84\"}],\"cohort\":\"rrf@0.03\",\"enabled\":true,\"installdate\":-1,\"lang\":\"en-US\",\"ping\":{\"r\":-2},\"targetingattributes\":{\"AppCohort\":\"rrf@0.03\",\"AppMajorVersion\":\"157\",\"AppRollout\":0.03,\"AppVersion\":\"157.0.4341.46\",\""
		"IsInternalUser\":false,\"Priority\":false,\"Updater\":\"Omaha\",\"UpdaterVersion\":\"1.3.315.17\"},\"updatecheck\":{},\"version\":\"2026.2.24.1\"},{\"appid\":\"kieecehchjjaaepgajdhcehijkehdenm\",\"brand\":\"EPBR\",\"cached_items\":[{\"sha256\":\"11249dd2052a07e104ef3c63b960d50aa8fcb79f0978fb9afb3a60ed4dc4ae63\"}],\"cohort\":\"rrf@0.17\",\"enabled\":true,\"installdate\":-1,\"lang\":\"en-US\",\"ping\":{\"r\":-2},\"targetingattributes\":{\"AppCohort\":\"rrf@0.17\",\"AppMajorVersion\":\"157\",\""
		"AppRollout\":0.17,\"AppVersion\":\"157.0.4341.46\",\"IsInternalUser\":false,\"Priority\":false,\"Updater\":\"Omaha\",\"UpdaterVersion\":\"1.3.315.17\"},\"updatecheck\":{},\"version\":\"2026.11.11.2\"},{\"appid\":\"jpinkpebmplndiafioikiciobeafamld\",\"brand\":\"EPBR\",\"cached_items\":[{\"sha256\":\"f081de18a604e95a175eaf4dd91b35b7f17ad4de24ee2f20eeb034c979bbcccb\"}],\"cohort\":\"rrf@0.18\",\"enabled\":true,\"installdate\":-1,\"lang\":\"en-US\",\"ping\":{\"r\":-2},\"targetingattributes\":{\""
		"AppCohort\":\"rrf@0.18\",\"AppMajorVersion\":\"157\",\"AppRollout\":0.18,\"AppVersion\":\"157.0.4341.46\",\"IsInternalUser\":false,\"Priority\":false,\"Updater\":\"Omaha\",\"UpdaterVersion\":\"1.3.315.17\"},\"updatecheck\":{},\"version\":\"2025.10.7.5\"},{\"appid\":\"jcmcegpcehdchljeldgmmfbgcpnmgedo\",\"brand\":\"EPBR\",\"cached_items\":[{\"sha256\":\"c6428e81ee4fd74e6b82f75f7571e725d56e935373cd02636e4711bad0e86975\"}],\"cohort\":\"rrf@0.50\",\"enabled\":true,\"installdate\":-1,\"lang\":\"en-US\","
		"\"ping\":{\"r\":-2},\"targetingattributes\":{\"AppCohort\":\"rrf@0.50\",\"AppMajorVersion\":\"157\",\"AppRollout\":0.5,\"AppVersion\":\"157.0.4341.46\",\"IsInternalUser\":false,\"Priority\":false,\"Updater\":\"Omaha\",\"UpdaterVersion\":\"1.3.315.17\"},\"updatecheck\":{},\"version\":\"2026.11.11.2\"},{\"appid\":\"npbipokbgmclmkjhfjicdgnedhkocjpl\",\"brand\":\"EPBR\",\"cached_items\":[{\"sha256\":\"c568b829155020d080a545f6b5796d36ace34a97b64cb4a09bb46980dd82da6a\"}],\"cohort\":\"rrf@0.38\",\""
		"enabled\":true,\"installdate\":-1,\"lang\":\"en-US\",\"model_locale\":\"en\",\"ping\":{\"r\":-2},\"targetingattributes\":{\"AppCohort\":\"rrf@0.38\",\"AppMajorVersion\":\"157\",\"AppRollout\":0.38,\"AppVersion\":\"157.0.4341.46\",\"IsInternalUser\":false,\"Priority\":false,\"Updater\":\"Omaha\",\"UpdaterVersion\":\"1.3.315.17\"},\"updatecheck\":{},\"version\":\"2026.10.19.3\"},{\"appid\":\"fmbfidpnnknmblionmcahabilfoageoe\",\"brand\":\"EPBR\",\"cached_items\":[{\"sha256\":\""
		"5a8a5a5d1f948d724847c005c9875507c34e5b76e73192fc1f2d22605fd69bd7\"}],\"cohort\":\"rrf@0.24\",\"enabled\":true,\"installdate\":-1,\"lang\":\"en-US\",\"ping\":{\"r\":-2},\"targetingattributes\":{\"AppCohort\":\"rrf@0.24\",\"AppMajorVersion\":\"157\",\"AppRollout\":0.24,\"AppVersion\":\"157.0.4341.46\",\"IsInternalUser\":false,\"Priority\":false,\"Updater\":\"Omaha\",\"UpdaterVersion\":\"1.3.315.17\"},\"updatecheck\":{},\"version\":\"2026.2.23.1\"},{\"appid\":\"eiihffpgcdgabdmcecnakaohbclgfbmb\",\""
		"brand\":\"EPBR\",\"cached_items\":[{\"sha256\":\"cdff9e6a793fd77b105ed2ef1bf1788c1820af7d6f283202385434487672be8f\"}],\"cohort\":\"rrf@0.85\",\"enabled\":true,\"installdate\":-1,\"lang\":\"en-US\",\"ping\":{\"r\":-2},\"targetingattributes\":{\"AppCohort\":\"rrf@0.85\",\"AppMajorVersion\":\"157\",\"AppRollout\":0.85,\"AppVersion\":\"157.0.4341.46\",\"IsInternalUser\":false,\"Priority\":false,\"Updater\":\"Omaha\",\"UpdaterVersion\":\"1.3.315.17\"},\"updatecheck\":{},\"version\":\"2026.3.4.1\"},{\""
		"appid\":\"lfmeghnikdkbonehgjihjebgioakijgn\",\"brand\":\"EPBR\",\"cached_items\":[{\"sha256\":\"31d91f33855ea925653c7ffab600fc786d79e28edc5c237d88f449db332b6cd0\"}],\"cohort\":\"rrf@0.85\",\"enabled\":true,\"installdate\":-1,\"lang\":\"en-US\",\"ping\":{\"r\":-2},\"targetingattributes\":{\"AppCohort\":\"rrf@0.85\",\"AppMajorVersion\":\"157\",\"AppRollout\":0.85,\"AppVersion\":\"157.0.4341.46\",\"IsInternalUser\":false,\"Priority\":false,\"Updater\":\"Omaha\",\"UpdaterVersion\":\"1.3.315.17\"},\""
		"updatecheck\":{},\"version\":\"2.0.0.160\"},{\"appid\":\"pbdgbpmpeenomngainidcjmopnklimmf\",\"brand\":\"EPBR\",\"cached_items\":[{\"sha256\":\"b27bec7581505715364f132de1998818c82462dbf55a1f55f9b15e29e988d791\"}],\"cohort\":\"rrf@0.50\",\"enabled\":true,\"installdate\":-1,\"lang\":\"en-US\",\"ping\":{\"r\":-2},\"targetingattributes\":{\"AppCohort\":\"rrf@0.50\",\"AppMajorVersion\":\"157\",\"AppRollout\":0.5,\"AppVersion\":\"157.0.4341.46\",\"IsInternalUser\":false,\"Priority\":false,\"Updater\":\""
		"Omaha\",\"UpdaterVersion\":\"1.3.315.17\"},\"updatecheck\":{},\"version\":\"0.0.0.46\"},{\"appid\":\"lkkdlcloifjinapabfonaibjijloebfb\",\"brand\":\"EPBR\",\"cached_items\":[{\"sha256\":\"7822e4838f023d1ec22a573b21a377708d726da87e3d0a91dc0bfabc063fd9a8\"}],\"cohort\":\"rrf@0.74\",\"enabled\":true,\"installdate\":-1,\"lang\":\"en-US\",\"ping\":{\"r\":-2},\"targetingattributes\":{\"AppCohort\":\"rrf@0.74\",\"AppMajorVersion\":\"157\",\"AppRollout\":0.74,\"AppVersion\":\"157.0.4341.46\",\""
		"IsInternalUser\":false,\"Priority\":false,\"Updater\":\"Omaha\",\"UpdaterVersion\":\"1.3.315.17\"},\"updatecheck\":{},\"version\":\"4.0.4.26\"},{\"appid\":\"hjaimielcgmceiphgjjfddlgjklfpdei\",\"brand\":\"EPBR\",\"cached_items\":[{\"sha256\":\"a00289af85d31d698a0f6753b6ce67dbab4bdff639bde5fc588a5d5d8a3885d5\"}],\"cohort\":\"rrf@0.31\",\"enabled\":true,\"installdate\":-1,\"lang\":\"en-US\",\"ping\":{\"r\":-2},\"targetingattributes\":{\"AppCohort\":\"rrf@0.31\",\"AppMajorVersion\":\"157\",\""
		"AppRollout\":0.31,\"AppVersion\":\"157.0.4341.46\",\"IsInternalUser\":false,\"Priority\":false,\"Updater\":\"Omaha\",\"UpdaterVersion\":\"1.3.315.17\"},\"updatecheck\":{},\"version\":\"1.0.0.5\"},{\"appid\":\"mkcgfaeepibomfapiapjaceihcojnphg\",\"brand\":\"EPBR\",\"cohort\":\"rrf@0.50\",\"enabled\":true,\"installdate\":-1,\"lang\":\"en-US\",\"ping\":{\"r\":-2},\"targetingattributes\":{\"AppCohort\":\"rrf@0.50\",\"AppMajorVersion\":\"157\",\"AppRollout\":0.5,\"AppVersion\":\"157.0.4341.46\",\""
		"IsInternalUser\":false,\"Priority\":false,\"Updater\":\"Omaha\",\"UpdaterVersion\":\"1.3.315.17\"},\"updatecheck\":{},\"version\":\"0.0.0.0\"},{\"accept_locale\":\"ENUS500000\",\"appid\":\"njaocnahcpjeeknehofkiijbojppiiki\",\"brand\":\"EPBR\",\"cohort\":\"rrf@0.33\",\"enabled\":true,\"installdate\":-1,\"lang\":\"en-US\",\"ping\":{\"r\":-2},\"targetingattributes\":{\"AppCohort\":\"rrf@0.33\",\"AppMajorVersion\":\"157\",\"AppRollout\":0.33,\"AppVersion\":\"157.0.4341.46\",\"IsInternalUser\":false,\""
		"Priority\":false,\"Updater\":\"Omaha\",\"UpdaterVersion\":\"1.3.315.17\"},\"updatecheck\":{},\"version\":\"0.0.0.0\"},{\"appid\":\"nmcnjaceoejcjmmnabjnmfpoanaengif\",\"brand\":\"EPBR\",\"cached_items\":[{\"sha256\":\"a9592ae40712c6cfdf7d142e2563ca4ec8f696cfe53e267ad0ea630c43beaa33\"}],\"cohort\":\"rrf@0.18\",\"enabled\":true,\"installdate\":-1,\"lang\":\"en-US\",\"ping\":{\"r\":-2},\"targetingattributes\":{\"AppCohort\":\"rrf@0.18\",\"AppMajorVersion\":\"157\",\"AppRollout\":0.18,\"AppVersion\":\""
		"157.0.4341.46\",\"IsInternalUser\":false,\"Priority\":false,\"Updater\":\"Omaha\",\"UpdaterVersion\":\"1.3.315.17\"},\"updatecheck\":{},\"version\":\"2026.1.30.1\"},{\"appid\":\"cllppcmmlnkggcmljjfigkcigaajjmid\",\"brand\":\"EPBR\",\"cached_items\":[{\"sha256\":\"38b9a60260c000df8eadd64719d86020e30480df9afb893e60b5ef7d780616a5\"}],\"cohort\":\"rrf@0.51\",\"enabled\":true,\"installdate\":-1,\"lang\":\"en-US\",\"ping\":{\"r\":-2},\"targetingattributes\":{\"AppCohort\":\"rrf@0.51\",\"AppMajorVersion"
		"\":\"157\",\"AppRollout\":0.51,\"AppVersion\":\"157.0.4341.46\",\"IsInternalUser\":false,\"Priority\":false,\"Updater\":\"Omaha\",\"UpdaterVersion\":\"1.3.315.17\"},\"updatecheck\":{},\"version\":\"128.18367.18366.1\"},{\"appid\":\"gghpafdlgdjgkjfihkmbhlkmdoagjnom\",\"brand\":\"EPBR\",\"cached_items\":[{\"sha256\":\"7dc2661880b00149372ddb07d9253e1cd9a11be1c99a69444930881759850eeb\"}],\"cohort\":\"rrf@0.50\",\"enabled\":true,\"installdate\":-1,\"lang\":\"en-US\",\"ping\":{\"r\":-2},\""
		"targetingattributes\":{\"AppCohort\":\"rrf@0.50\",\"AppMajorVersion\":\"157\",\"AppRollout\":0.5,\"AppVersion\":\"157.0.4341.46\",\"IsInternalUser\":false,\"Priority\":false,\"Updater\":\"Omaha\",\"UpdaterVersion\":\"1.3.315.17\"},\"updatecheck\":{},\"version\":\"2026.9.20.1\"},{\"appid\":\"pdfjdcjjjegpclfiilihfkmdfndkneei\",\"brand\":\"EPBR\",\"cohort\":\"rrf@0.91\",\"enabled\":true,\"installdate\":-1,\"lang\":\"en-US\",\"ping\":{\"r\":-2},\"targetingattributes\":{\"AppCohort\":\"rrf@0.91\",\""
		"AppMajorVersion\":\"157\",\"AppRollout\":0.91,\"AppVersion\":\"157.0.4341.46\",\"IsInternalUser\":false,\"Priority\":false,\"Updater\":\"Omaha\",\"UpdaterVersion\":\"1.3.315.17\"},\"updatecheck\":{},\"version\":\"2025.7.24.0\"}],\"arch\":\"x64\",\"dedup\":\"cr\",\"domainjoined\":false,\"hw\":{\"avx\":1,\"physmemory\":31,\"sse\":1,\"sse2\":1,\"sse3\":1,\"sse41\":1,\"sse42\":1,\"ssse3\":1},\"ismachine\":1,\"os\":{\"arch\":\"x86_64\",\"deviceformfactor\":\"desktop\",\"platform\":\"Windows\",\""
		"version\":\"10.0.26300.9974\"},\"prodversion\":\"157.0.4341.46\",\"protocol\":\"4.0\",\"requestid\":\"{a73f7d3d-0763-4c28-8085-3398f6966f1b}\",\"sessionid\":\"{868ec324-ec4b-4e76-8694-d3f666487bdf}\",\"updaters\":{\"autoupdatecheckenabled\":true,\"ismachine\":1,\"lastchecked\":0,\"laststarted\":0,\"name\":\"Omaha\",\"updatepolicy\":-1,\"version\":\"1.3.315.17\"},\"updaterversion\":\"157.0.4341.46\"}}", 
		EXTRARES, 
		"Url=https://www.tangerine.ca/etc.clientlibs/tangerine/clientlibs/clientlib-site/resources/fonts/tangerine-circular/lineto-tangerinecircular-book.woff", "Referer=https://www.tangerine.ca/etc.clientlibs/tangerine/clientlibs/clientlib-site.lc-548a3a3dd9416446a4c03659772d3bef-lc.min.css", ENDITEM, 
		"Url=https://www.tangerine.ca/content/dam/tangerine-shared/icons/icon-percent-light.svg", "Referer=https://www.tangerine.ca/etc.clientlibs/tangerine/clientlibs/clientlib-site.lc-548a3a3dd9416446a4c03659772d3bef-lc.min.css", ENDITEM, 
		"Url=https://www.tangerine.ca/content/dam/tangerine-shared/icons/icon-feedback-light.svg", "Referer=https://www.tangerine.ca/etc.clientlibs/tangerine/clientlibs/clientlib-site.lc-548a3a3dd9416446a4c03659772d3bef-lc.min.css", ENDITEM, 
		"Url=https://sdk.asapp.com/chat-sdk.js", "Referer=https://www.tangerine.ca/", ENDITEM, 
		"Url=https://www.tangerine.ca/etc.clientlibs/tangerine/clientlibs/clientlib-site/resources/fonts/tangerine-circular/lineto-tangerinecircular-medium.woff", "Referer=https://www.tangerine.ca/etc.clientlibs/tangerine/clientlibs/clientlib-site.lc-548a3a3dd9416446a4c03659772d3bef-lc.min.css", ENDITEM, 
		"Url=https://www.tangerine.ca/etc.clientlibs/tangerine/clientlibs/clientlib-site/resources/fonts/tangerine-circular/TangerineCircular-Bold.woff", "Referer=https://www.tangerine.ca/etc.clientlibs/tangerine/clientlibs/clientlib-site.lc-548a3a3dd9416446a4c03659772d3bef-lc.min.css", ENDITEM, 
		LAST);

	web_add_auto_header("Sec-Fetch-Site", 
		"cross-site");

	web_add_header("Origin", 
		"https://www.tangerine.ca");

	web_add_auto_header("Sec-Fetch-Mode", 
		"cors");

	web_add_auto_header("sec-ch-ua", 
		"\"Not-A.Brand\";v=\"99\", \"Microsoft Edge\";v=\"157\", \"Chromium\";v=\"157\"");

	web_add_auto_header("sec-ch-ua-mobile", 
		"?0");

	web_add_auto_header("sec-ch-ua-platform", 
		"\"Windows\"");

	lr_think_time(5);

	web_url("location", 
		"URL=https://geolocation.onetrust.com/cookieconsentpub/v1/geo/location", 
		"Resource=0", 
		"RecContentType=application/json", 
		"Referer=https://www.tangerine.ca/", 
		"Snapshot=t11.inf", 
		"Mode=HTML", 
		EXTRARES, 
		"Url=https://cdn.schemaapp.com/javascript/highlight.js", "Referer=https://www.tangerine.ca/", ENDITEM, 
		LAST);

	web_add_auto_header("Sec-Fetch-Site", 
		"same-origin");

/*Correlation comment - Do not change!  Original value='0784AACF5A857A4D109C851D4E2B06C7~YAAQD5YqF2WHXcOhAQAA9lQKzQHFhHuB4w94JXhFLA/h5bundM9YYbwct+II/pK77H3HxLBFLw7SxEVxHNTu4KU23Jom9qEr9ISsGlqkUUHxIk/bbrvmmlBh3tCj5I/ImBpm4IvrNnhq9UnfxS3UWk5cjU2xGsPFn3GNIPyivzrkICVrBpsH/kCLJ8Mqbew8xbhPzAluOCxpuhhrqCr464gRu8ZRNGFA18B+fCiC798sMtN5UOmYQUWUKN7FoJZo5AY=~1' Name ='bm_sv' Type ='ResponseBased'*/
	web_reg_save_param_regexp(
		"ParamName=bm_sv",
		"RegExp=bm_sv=(.*?);",
		SEARCH_FILTERS,
		"Scope=Cookies",
		"IgnoreRedirections=No",
		LAST);

/*Correlation comment - Do not change!  Original value='k1379hwcxORwhvT1gledVrA6rTZ5mudi' Name ='appId' Type ='ResponseBased'*/
	web_reg_save_param_json(
		"ParamName=appId",
		"QueryString=$.calculator_portfolio_performance_appID",
		SEARCH_FILTERS,
		"Scope=Body",
		"IgnoreRedirections=No",
		LAST);

/*Correlation comment - Do not change!  Original value='Google+Symbols:wght,FILL,ROND@300..400,0..1,0..100' Name ='family' Type ='ResponseBased'*/
	web_reg_save_param_regexp(
		"ParamName=family",
		"RegExp=family=(.*?)&display",
		SEARCH_FILTERS,
		"Scope=Body",
		"IgnoreRedirections=No",
		"RequestUrl=*/m=bootstrap_module,ucs_widget_module,xlite_module*",
		LAST);

/*Correlation comment - Do not change!  Original value='Google+Sans:wght@400' Name ='family_1' Type ='ResponseBased'*/
	web_reg_save_param_regexp(
		"ParamName=family_1",
		"RegExp=family=(.*?);500",
		SEARCH_FILTERS,
		"Scope=Body",
		"IgnoreRedirections=No",
		"RequestUrl=*/m=bootstrap_module,ucs_widget_module,xlite_module*",
		LAST);

/*Correlation comment - Do not change!  Original value='Google+Sans+Flex:opsz,slnt,wdth,wght,GRAD,ROND@13..56,-10..0,92..100,250..520,0,0..100' Name ='family_2' Type ='ResponseBased'*/
	web_reg_save_param_regexp(
		"ParamName=family_2",
		"RegExp=family=(.*?)&display",
		"Ordinal=2",
		SEARCH_FILTERS,
		"Scope=Body",
		"IgnoreRedirections=No",
		"RequestUrl=*/m=bootstrap_module,ucs_widget_module,xlite_module*",
		LAST);

/*Correlation comment - Do not change!  Original value='Google+Sans+Text:wght@400' Name ='family_3' Type ='ResponseBased'*/
	web_reg_save_param_regexp(
		"ParamName=family_3",
		"RegExp=family=(.*?);500",
		"Ordinal=2",
		SEARCH_FILTERS,
		"Scope=Body",
		"IgnoreRedirections=No",
		"RequestUrl=*/m=bootstrap_module,ucs_widget_module,xlite_module*",
		LAST);

/*Correlation comment - Do not change!  Original value='Google+Sans+Mono:ital,wght@0,300..800' Name ='family_4' Type ='ResponseBased'*/
	web_reg_save_param_regexp(
		"ParamName=family_4",
		"RegExp=family=(.*?);1,300\\.\\.800`,\\(0,_\\.ck\\)`https:",
		SEARCH_FILTERS,
		"Scope=Body",
		"IgnoreRedirections=No",
		"RequestUrl=*/m=bootstrap_module,ucs_widget_module,xlite_module*",
		LAST);

	web_url("global.json", 
		"URL=https://www.tangerine.ca/etc.clientlibs/tangerine/clientlibs/clientlib-site/resources/conf/global.json", 
		"Resource=0", 
		"RecContentType=application/json", 
		"Referer=https://www.tangerine.ca/en/personal", 
		"Snapshot=t12.inf", 
		"Mode=HTML", 
		EXTRARES, 
		"Url=/content/dam/tangerine-shared/icons/icon-circle-check-light.svg", "Referer=https://www.tangerine.ca/etc.clientlibs/tangerine/clientlibs/clientlib-site.lc-548a3a3dd9416446a4c03659772d3bef-lc.min.css", ENDITEM, 
		"Url=/content/dam/tangerine-shared/icons/icon-chevron-up-light.svg", "Referer=https://www.tangerine.ca/etc.clientlibs/tangerine/clientlibs/clientlib-site.lc-548a3a3dd9416446a4c03659772d3bef-lc.min.css", ENDITEM, 
		"Url=https://www.googletagmanager.com/gtm.js?id=GTM-MLWBHX9W&gtg_health=1", "Referer=https://www.tangerine.ca/", ENDITEM, 
		"Url=https://www.gstatic.com/_/mss/boq-cloud-ai-ucs/_/js/k=boq-cloud-ai-ucs.UcsWidgetUi.en_US.k6P3Ekz2bpI.2021.O/am=AAAAGGA/d=1/rs=AAj4NmzRTyclRzxqiI7J-mq78SXNqvmAIA/m=bootstrap_module,ucs_widget_module,xlite_module", "Referer=https://www.tangerine.ca/", ENDITEM, 
		LAST);

	web_add_header("Origin", 
		"https://www.tangerine.ca");

	web_custom_request("4MwpSUxM", 
		"URL=https://www.tangerine.ca/XzdnU1ENiZ-tP/yP2ljgJg/3OjS5E/YD5zScrwS8QpJc/MzF7RW8hCA/Oj9/4MwpSUxM", 
		"Method=POST", 
		"Resource=0", 
		"RecContentType=application/json", 
		"Referer=https://www.tangerine.ca/en/personal", 
		"Snapshot=t13.inf", 
		"Mode=HTML", 
		"EncType=text/plain;charset=UTF-8", 
		"Body={\"sensor_data\":\"3;0;1;0;4405057;+42GUhFh6owSFeuhdnWqmVpUMPcVF8nRj8KyP7mzv+I=;36,0,0,0,3,0;5=oe\\\"WP;\\\"u\\\"3Hr:\\\"E;N\\\"DJ\\\"~Jr\\\"L`\\\"gz<_~\\\">(;b\\\"^Ty\\\"S*h\\\"cPT\\\"0#5\\\"l`C{s\\\"P5N/\\\"$Dm\\\"dqu\\\":k44U\\\"rR+S\\\"&\\\"i{y@/\\\"I7F-F(jtQ/Jg$C3k\\\"a\\\"ua<\\\"8B*go{H]ChOwRmJ;P \\\"cu]\\\">\\\"w\\\"C4s\\\"ux%\\\".\\\"\\\"r\\\"P)s\\\"P\\\"k)VcW\\\"P8^\\\"-%r\\\"3\\\"P\\\"C\\\"6q \\\"GeEOVwib/-R<\\\"<I4\\\"4\\\"uc}\\\"c\\\"NqB\\\"Ha}:y\\\")z\\\"o8[%9\\\")4K\\\"GH4rd(I;"
		"s\\\"u!y\\\"o\\\"`/*dcH@rZl:*1M\\\"NB:\\\"K0X\\\"o\\\"\\\"k\\\"rv6\\\"g\\\"\\\"p\\\"A8r\\\"Qgoa\\\"7H}\\\"T\\\"r+,1\\\"k\\\"?OQ\\\"mR7igZu\\\"\\\"6\\\"nr+\\\"RH+.)Ly=?E~3R\\\"1/m\\\"H&~rw\\\"XG\\\"/\\\"HJ\\\"~\\\"Uqp\\\"r*24#w&\\\"=*XmF7[L<|BHwi\\\"|\\\"`@8\\\"vv\\\"H v\\\"0!_\\\"/4u7M;QKZl|iI;o\\\",qTTu\\\"S}Aj{=A_1d:6\\\"JRLU\\\"A\\\"QJPGBmcn*s$0, U|0c[{h> {[J[UdMI@i;Ub.114r<b3\\\"l\\\"MvI\\\"1}]4H\\\"o}p\\\"y53XR\\\"*9N\\\":-5Yr\\\"p)\\\"a\\\"h:F)S%q!H?oq>+^o|mk>r?:4J0O5tD:4H;21Os3v-0uk2TwjA0t^"
		"Cfi*E{MHhS?(TttO}C98Q$xP$P)Te&P:ptq`,kB5kZ-x<Q/L,Y|sYrHyFjJN<TenJbq3]D!oW\\\"{k/\\\"XYX\\\"f\\\"3= \\\"5\\\"s-f\\\"ENZv Z)xPP<cp\\\"$<V\\\"!dq\\\"/V9\\\"y7#/Wj.`7_vG/ugUsA(OW:z{ZQltE_[\\\";\\\"9c>\\\"7\\\"e\\\"3HC[\\\"\\\"5\\\"lbE\\\"f|tWdu|G,If@\\\"/i-L:5Ws5><)3%ba:eL}ef^|lry4Rm>O[g^Fz9I}OW\\\"HiQ\\\"T]1\\\"|>HJqqp/\\\"g]V\\\"K)Oh\\\"SrY\\\"W\\\"\\\"b\\\"cSq\\\"!\\\"\\\"n\\\"#>\\\"<8l W\\\"=&F\\\"B\\\"\\\"?\\\"|y3\\\"x#-E04G7#\\\"[t\\\"$\\\"\\\"h9t\\\"0$\\\"hi/ig\\\"dr5\\\"  >::]@=\\\"|UL\\\""
		"dMTNU\\\"-dZ\\\"!&|\\\"w*@k\\\"l\\\"\\\"-\\\"K=E\\\"^/ zu\\\"{y#p\\\"}\\\"r{iMNZ|3\\\"[B=\\\"O]P\\\"tr\\\"%C?S\\\"}\\\"\\\"r\\\":,4\\\"lKma05~*\\\"g>3\\\"T>J}S\\\"/*TK\\\"CSSM8\\\"4TH\\\"jY\\\"6s2\\\"V\\\"\\\":+r\\\"NB7\\\"Y\\\"3M` Jk_n*aV+9Wok.S4EU4PP<>TG3Q;Rn)w.4VC6krnbvhh4xY$$Sl\\\")\\\"1fU\\\"AAc{G\\\"}t\\\"i\\\"+SbV%=!E:mV&[\\\"E\\\"-^D\\\"cq*PuKt.FS\\\"Np]\\\"-R}H$i\\\".XQk\\\"b\\\">\\\"nr+\\\"qBg\\\"4KV@v\\\"il}\\\"I\\\"\\\"F>{\\\"4j(\\\"wK)\\\"}9W\\\"3v.h~\\\"HQ*\\\"^U)>#9\\\"po\\\"*j9\\\""
		"R)o1\\\",\\\"9%lM*\\\"/NY\\\"|+@\\\"&lP\\\"|y`\\\"],)Y;\\\"3B}<\\\"vh>{M/&D.\\\"v=)\\\"{kl@_=\\\"b=a!bd+\\\">g;|j\\\",]<E\\\"!R\\\"<lW\\\"qpq#qnT3R$tv)IvSB\\\"b<>\\\"u4Q\\\"+^{\\\"vsdxkunp\\\"+c*\\\"Gk+\\\"){a\\\"ra8q)KukD\\\"@,50\\\"nz{\\\"a<{\\\"sv=OC|\\\"EQH@\\\":\\\"CdeHK\\\"r/ \\\"1]Xet\\\"L{){b..T[O\\\"3:$b\\\">\\\"\\\"s[A\\\"BKi\\\"fb)ux6!#\\\"h)|\\\">1D;: {F\\\"u9/\\\"s\\\"\\\".\\\"@wz\\\"g\\\"C\\\"&Aq\\\"8!5\\\"wg|D@K\\\"j8s[l2:OZ s\\\"\\\"9\\\"kSe\\\"=\\\"lY\\\"k5z\\\"$rWF\\\"H(f\\\""
		"m2D\\\"j52ha\\\"Q3\\\"\"}", 
		EXTRARES, 
		"Url=/content/dam/icons/icon-flip-light.svg", "Referer=https://www.tangerine.ca/etc.clientlibs/tangerine/clientlibs/clientlib-site.lc-548a3a3dd9416446a4c03659772d3bef-lc.min.css", ENDITEM, 
		LAST);

	web_url("en.json", 
		"URL=https://www.tangerine.ca/etc.clientlibs/tangerine/clientlibs/clientlib-onetrust/resources/oneTrust/consent/abe5e4e6-b00b-4dc8-aa66-ea460fe6a634/0195aa99-ba4d-7be7-a2d8-6fae40dd9ed4/en.json", 
		"Resource=0", 
		"RecContentType=application/json", 
		"Referer=https://www.tangerine.ca/en/personal", 
		"Snapshot=t14.inf", 
		"Mode=HTML", 
		LAST);

	web_add_cookie("bm_sv={bm_sv}; DOMAIN=www.tangerine.ca");

	web_url("currentRates.json", 
		"URL=https://www.tangerine.ca/content/dam/tangerine-shared/product-rates/currentRates.json", 
		"Resource=0", 
		"RecContentType=application/json", 
		"Referer=https://www.tangerine.ca/en/personal", 
		"Snapshot=t15.inf", 
		"Mode=HTML", 
		LAST);

	web_url("token.json", 
		"URL=https://www.tangerine.ca/libs/granite/csrf/token.json", 
		"Resource=0", 
		"RecContentType=application/json", 
		"Referer=https://www.tangerine.ca/en/personal", 
		"Snapshot=t16.inf", 
		"Mode=HTML", 
		LAST);

	web_url("currentNCORates.json", 
		"URL=https://www.tangerine.ca/content/dam/tangerine-shared/product-rates/currentNCORates.json", 
		"Resource=0", 
		"RecContentType=application/json", 
		"Referer=https://www.tangerine.ca/en/personal", 
		"Snapshot=t17.inf", 
		"Mode=HTML", 
		EXTRARES, 
		"Url=https://sdk.asapp.com/chat-sdk.css", "Referer=https://www.tangerine.ca/", ENDITEM, 
		LAST);

	web_add_auto_header("Sec-Fetch-Site", 
		"cross-site");

	web_add_auto_header("Origin", 
		"https://www.tangerine.ca");

	web_add_header("Sec-Fetch-Storage-Access", 
		"none");

	web_custom_request("id", 
		"URL=https://dpm.demdex.net/id?d_visid_ver=5.5.0&d_fieldgroup=MC&d_rtbd=json&d_ver=2&d_orgid=0AAF22CE52827A080A490D4D%40AdobeOrg&d_nsid=0&ts=1794441370359", 
		"Method=GET", 
		"Resource=0", 
		"RecContentType=application/json", 
		"Referer=https://www.tangerine.ca/", 
		"Snapshot=t18.inf", 
		"Mode=HTML", 
		"EncType=application/x-www-form-urlencoded", 
		EXTRARES, 
		"Url=http://cacerts.digicert.com/DigiCertEVRSACAG2.crt", "Referer=", ENDITEM, 
		LAST);

	web_add_cookie("_ga_RFBV4QJDD5=GS2.1.s1794441370$o1$g0$t1794441370$j60$l0$h0$dKHzV4V9--bXAjQxlczQ8X0FRhgVwTKOpdA; DOMAIN=www.tangerine.ca");

	web_add_cookie("_ga=GA1.1.1478828077.1794441375; DOMAIN=www.tangerine.ca");

	web_add_auto_header("Sec-Fetch-Site", 
		"same-origin");

	web_add_header("CSRF-Token",
		"{CorrelationParameter}");

	web_custom_request("pixel_16cf6b81", 
		"URL=https://www.tangerine.ca/akam/13/pixel_16cf6b81", 
		"Method=POST", 
		"Resource=0", 
		"RecContentType=text/html", 
		"Referer=https://www.tangerine.ca/en/personal", 
		"Snapshot=t19.inf", 
		"Mode=HTML", 
		"Body=ap=true&bt=%7B%22charging%22%3Atrue%2C%22chargingTime%22%3A%22Infinity%22%2C%22dischargingTime%22%3A%22Infinity%22%2C%22level%22%3A0.98%2C%22onchargingchange%22%3Anull%2C%22onchargingtimechange%22%3Anull%2C%22ondischargingtimechange%22%3Anull%2C%22onlevelchange%22%3Anull%7D&fonts=null&fh=null&timing="
		"%7B%221%22%3A23%2C%222%22%3A4814%2C%22profile%22%3A%7B%22bp%22%3A1%2C%22sr%22%3A0%2C%22dp%22%3A0%2C%22lt%22%3A0%2C%22ps%22%3A0%2C%22cv%22%3A16%2C%22fp%22%3A0%2C%22sp%22%3A1%2C%22br%22%3A0%2C%22ieps%22%3A0%2C%22av%22%3A0%2C%22z1%22%3A4%2C%22jsv%22%3A0%2C%22nav%22%3A0%2C%22nap%22%3A1%2C%22crc%22%3A0%2C%22z2%22%3A1%7D%2C%22main%22%3A47008%2C%22compute%22%3A23%2C%22send%22%3A4814%7D&bp="
		"2087755996%2C1953464915%2C591862434%2C325835597%2C1068473606%2C-1382186647%2C-365096851%2C-1979186206%2C-108039040%2C-1906852049&sr=%7B%22inner%22%3A%5B1912%2C964%5D%2C%22outer%22%3A%5B1920%2C1048%5D%2C%22screen%22%3A%5B0%2C0%5D%2C%22pageOffset%22%3A%5B0%2C0%5D%2C%22avail%22%3A%5B1920%2C1048%5D%2C%22size%22%3A%5B1920%2C1080%5D%2C%22client%22%3A%5B1897%2C9061%5D%2C%22colorDepth%22%3A24%2C%22pixelDepth%22%3A24%7D&dp="
		"%7B%22XDomainRequest%22%3A0%2C%22createPopup%22%3A0%2C%22removeEventListener%22%3A1%2C%22globalStorage%22%3A0%2C%22openDatabase%22%3A0%2C%22indexedDB%22%3A1%2C%22attachEvent%22%3A0%2C%22ActiveXObject%22%3A0%2C%22dispatchEvent%22%3A1%2C%22addBehavior%22%3A0%2C%22addEventListener%22%3A1%2C%22detachEvent%22%3A0%2C%22fireEvent%22%3A0%2C%22MutationObserver%22%3A1%2C%22HTMLMenuItemElement%22%3A0%2C%22Int8Array%22%3A1%2C%22postMessage%22%3A1%2C%22querySelector%22%3A1%2C%22getElementsByClassName%22%3A1%2C"
		"%22images%22%3A1%2C%22compatMode%22%3A%22CSS1Compat%22%2C%22documentMode%22%3A0%2C%22all%22%3A1%2C%22now%22%3A1%2C%22contextMenu%22%3A0%7D&lt=1794441370439-5&ps=true%2Ctrue&cv=8e1ce9287860155577d5ff7da2a6fa2acec654bb&fp=false&sp=false&br=Chrome&ieps=false&av=false&z=%7B%22a%22%3A382692112%2C%22b%22%3A1%2C%22c%22%3A1%7D&zh=&jsv=1.5&nav=%7B%22userAgent%22%3A%22Mozilla%2F5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)"
		"%20Chrome%2F157.0.0.0%20Safari%2F537.36%20Edg%2F157.0.0.0%22%2C%22appName%22%3A%22Netscape%22%2C%22appCodeName%22%3A%22Mozilla%22%2C%22appVersion%22%3A%225.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)"
		"%20Chrome%2F157.0.0.0%20Safari%2F537.36%20Edg%2F157.0.0.0%22%2C%22appMinorVersion%22%3A0%2C%22product%22%3A%22Gecko%22%2C%22productSub%22%3A%2220030107%22%2C%22vendor%22%3A%22Google%20Inc.%22%2C%22vendorSub%22%3A%22%22%2C%22buildID%22%3A0%2C%22platform%22%3A%22Win32%22%2C%22oscpu%22%3A0%2C%22hardwareConcurrency%22%3A14%2C%22language%22%3A%22en-US%22%2C%22languages%22%3A%5B%22en-US%22%2C%22en%22%5D%2C%22systemLanguage%22%3A0%2C%22userLanguage%22%3A0%2C%22doNotTrack%22%3Anull%2C%22msDoNotTrack%22%3A"
		"0%2C%22cookieEnabled%22%3Atrue%2C%22geolocation%22%3A1%2C%22vibrate%22%3A1%2C%22maxTouchPoints%22%3A10%2C%22webdriver%22%3Afalse%2C%22plugins%22%3A%5B%22PDF%20Viewer%22%2C%22Chrome%20PDF%20Viewer%22%2C%22Chromium%20PDF%20Viewer%22%2C%22Microsoft%20Edge%20PDF%20Viewer%22%2C%22WebKit%20built-in%20PDF%22%5D%7D&crc="
		"%7B%22window.chrome%22%3A%7B%22app%22%3A%7B%22isInstalled%22%3Afalse%2C%22InstallState%22%3A%7B%22DISABLED%22%3A%22disabled%22%2C%22INSTALLED%22%3A%22installed%22%2C%22NOT_INSTALLED%22%3A%22not_installed%22%7D%2C%22RunningState%22%3A%7B%22CANNOT_RUN%22%3A%22cannot_run%22%2C%22READY_TO_RUN%22%3A%22ready_to_run%22%2C%22RUNNING%22%3A%22running%22%7D%7D%7D%7D&t=e35e6d16135e063bd565b44516792357305565b1&u=c85fc3f9beac5343a65355af189a0323", 
		LAST);

	web_revert_auto_header("sec-ch-ua");

	web_revert_auto_header("sec-ch-ua-mobile");

	web_revert_auto_header("sec-ch-ua-platform");

	web_add_auto_header("Sec-Fetch-Site", 
		"same-site");

	web_add_header("Access-Control-Request-Headers", 
		"interact-sessionid");

	web_add_header("Access-Control-Request-Method", 
		"GET");

	web_custom_request("insights",
		"URL=https://api.tangerine.ca/mkt//v1/campaign/insights?interaction-point={interaction-point}&count=2&appId={appId}&audienceLevel=Anonymous&channel=FBEWeb&aid=540615",
		"Method=OPTIONS",
		"Resource=0",
		"Referer=https://www.tangerine.ca/",
		"Snapshot=t20.inf",
		"Mode=HTML",
		LAST);

	web_add_cookie("ak_bmsc={ak_bmsc}; DOMAIN=www.tangerine.ca");

	web_add_auto_header("Sec-Fetch-Site", 
		"same-origin");

	web_add_auto_header("Sec-Fetch-Mode", 
		"no-cors");

	web_add_auto_header("sec-ch-ua", 
		"\"Not-A.Brand\";v=\"99\", \"Microsoft Edge\";v=\"157\", \"Chromium\";v=\"157\"");

	web_add_auto_header("sec-ch-ua-mobile", 
		"?0");

	web_add_auto_header("sec-ch-ua-platform", 
		"\"Windows\"");

	web_custom_request("c", 
		"URL=https://www.tangerine.ca/evtservvs/ga/g/c?v=2&tid=G-RFBV4QJDD5&gtm=45g92e6ba1v878796413z89174847117za20kzb9174847117zd9174847117xf4&_p=1794441323654&gcs=G101&gcd=13p3t3p3p7l1&npa=1&dma_cps=-&dma=0&gdid=dNWVlNT&_eu=AAAAACAC&_uip=%3A%3A&cid=1478828077.1794441375&fp=1&frm=0&ibt=1&ngs=1&pscdl=denied&rcb=16&sr=1920x1080&uaa=x86&uab=64&uafvl=Not-A.Brand%3B99.0.0.0%7CMicrosoft%2520Edge%3B157.0.4341.46%7CChromium%3B157.0.8103.39&uam=&uamb=0&uap=Windows&uapv=19.0.0&uaw=0&ul=en-us&ur=CA-ON&_gsid="
		"KHzV4V9--bXAjQxlczQ8X0FRhgVwTKOpdA&_s=1&tag_exp=115938466~115938468~118897920~118897930~120213116~120385422~120412528~120420416~120469145~120469153~121246026~121246034~123329123~124170881&dl=https%3A%2F%2Fwww.tangerine.ca%2Fen%2Fpersonal&dp=%2Fen%2Fpersonal&sid=1794441370&sct=1&seg=0&dt=Personal%20Banking%20Online%3A%20Digital%20Banking%20in%20Canada%20%7C%20Tangerine&gtb=3&_tu=CAg&en=page_view&_fv=1&_nsi=1&_ss=1&gap.gtb=3&gap.gtbd=23&ep.gtm_tag_name=GA4%20-%20AEM%20-%20page_view&ep.tracking_optin"
		"=C0001%3A1%2CC0003%3A0%2CC0002%3A0%2CC0004%3A0&ep.user_agent_string=Mozilla%2F5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F157.0.0.0%20Safari%2F537.36%20Edg%2F157.0.0.0&ep.gtm_container_id=GTM-MLWBHX9W&ep.gtm_container_version=70&ep.timestamp=2026-11-11T18%3A56%3A00.654-05%3A00&ep.client_id_2=not%20set&ep.content_language=en&ep.previous_page_url=&ep.account_type=personal&ep.page_name=personal&ep.page_hostname=www.tangerine.ca&"
		"ep.previous_page_path=&ep.previous_page_hostname=&ep.content_group=visitor-web&ep.adobe_ecid=&ep.aem_template=tangerine-homepage&ep.aem_element_type=tangerine%2Fcomponents%2Fpage&ep.aem_element_id=page-00b74ac1ca&ep.aem_modify_date=2026-11-06T18%3A29%3A26Z&ep.aem_page_id=page-00b74ac1ca&up.user_login_status=logged-out&up.user_status=visitor&up.user_type=personal&up.user_consent_perf=No&up.user_consent_func=No&up.user_consent_target=No&tfd=96586", 
		"Method=POST", 
		"Resource=0", 
		"RecContentType=text/plain", 
		"Referer=https://www.tangerine.ca/en/personal", 
		"Snapshot=t21.inf", 
		"Mode=HTML", 
		"EncType=", 
		LAST);

	web_add_auto_header("Sec-Fetch-Site", 
		"same-site");

	web_add_auto_header("Sec-Fetch-Mode", 
		"cors");

	web_add_header("interact-sessionid", 
		"");

	web_url("insights_2",
		"URL=https://api.tangerine.ca/mkt//v1/campaign/insights?interaction-point={interaction-point}&count=2&appId={appId}&audienceLevel=Anonymous&channel=FBEWeb&aid=540615",
		"Resource=0",
		"RecContentType=application/json",
		"Referer=https://www.tangerine.ca/",
		"Snapshot=t22.inf",
		"Mode=HTML",
		LAST);

	web_revert_auto_header("Origin");

	web_add_auto_header("Sec-Fetch-Mode", 
		"navigate");

	web_add_auto_header("Sec-Fetch-Dest", 
		"iframe");

	web_add_auto_header("Sec-Fetch-Site", 
		"cross-site");

	web_add_auto_header("Sec-Fetch-Storage-Access", 
		"none");

	web_add_header("Upgrade-Insecure-Requests", 
		"1");

	web_url("dest5.html", 
		"URL=https://scotiabank.demdex.net/dest5.html?d_nsid=0", 
		"Resource=0", 
		"RecContentType=text/html", 
		"Referer=https://www.tangerine.ca/", 
		"Snapshot=t23.inf", 
		"Mode=HTML", 
		LAST);

	web_add_auto_header("Sec-Fetch-Mode", 
		"no-cors");

	web_add_header("Origin", 
		"https://www.tangerine.ca");

	web_add_auto_header("Sec-Fetch-Dest", 
		"empty");

	web_custom_request("collect", 
		"URL=https://www.google-analytics.com/g/s/collect?v=2&_gsid=KHzV4V9--bXAjQxlczQ8X0FRhgVwTKOpdA&gtm=45g92e6ba1v878796413z89174847117za20kzb9174847117zd9174847117xf4", 
		"Method=POST", 
		"Resource=0", 
		"RecContentType=text/plain", 
		"Referer=https://www.tangerine.ca/", 
		"Snapshot=t24.inf", 
		"Mode=HTML", 
		"EncType=", 
		LAST);

	web_add_cookie("AMCVS_0AAF22CE52827A080A490D4D%40AdobeOrg=1; DOMAIN=www.tangerine.ca");

	web_add_cookie("AMCV_0AAF22CE52827A080A490D4D%40AdobeOrg=179643557%7CMCIDTS%7C20769%7CMCMID%7C86123182909378347043684817210902965393%7CMCAAMLH-1795046175%7C9%7CMCAAMB-1795046175%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1794448576s%7CNONE%7CvVersion%7C5.5.0; DOMAIN=www.tangerine.ca");

	web_add_cookie("OptanonConsent=isGpcEnabled=0&datestamp=Wed+Nov+11+2026+18%3A56%3A39+GMT-0500+(Eastern+Standard+Time)&version=202502.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&landingPath=https%3A%2F%2Fwww.tangerine.ca%2Fen%2Fpersonal; DOMAIN=www.tangerine.ca");

	web_revert_auto_header("Sec-Fetch-Storage-Access");

	web_add_auto_header("Sec-Fetch-Mode", 
		"cors");

	web_add_auto_header("Sec-Fetch-Site", 
		"same-origin");

	lr_think_time(4);

	web_url("otFlat.json", 
		"URL=https://www.tangerine.ca/etc.clientlibs/tangerine/clientlibs/clientlib-onetrust/resources/oneTrust/scripttemplates/202502.1.0/assets/otFlat.json", 
		"Resource=0", 
		"RecContentType=application/json", 
		"Referer=https://www.tangerine.ca/en/personal", 
		"Snapshot=t25.inf", 
		"Mode=HTML", 
		LAST);

	web_add_cookie("bm_sv=0784AACF5A857A4D109C851D4E2B06C7~YAAQD5YqFyeOXcOhAQAAemwKzQGQfIXD6w6wUJnchHv+JNaOnw7nQFeULCJDVeaq5c1aB4wsrTExRzE91X7zQ01KOrBilp/m5LiiFO9sSWd9zFRi2gXtIZuWCjO/AwJ8kCRKKfrHW9jWp+04aWUYmOvfZkWr1/qdcqMxd0q4bWR5Dl/f6s7SLje8uCVhk0IR8EBvB1Oxe9OJXy5ZgIE7Gieuzkb2J3XYO4+I0lWLs1eF90Teq+aDQ09sV83vgJ7d/ww=~1; DOMAIN=www.tangerine.ca");

	web_url("otPcCenter.json", 
		"URL=https://www.tangerine.ca/etc.clientlibs/tangerine/clientlibs/clientlib-onetrust/resources/oneTrust/scripttemplates/202502.1.0/assets/v2/otPcCenter.json", 
		"Resource=0", 
		"RecContentType=application/json", 
		"Referer=https://www.tangerine.ca/en/personal", 
		"Snapshot=t26.inf", 
		"Mode=HTML", 
		LAST);

	web_url("master.html", 
		"URL=https://www.tangerine.ca/content/experience-fragments/tangerine/ca/insights/en/hpoi320gic/homepage-banner/master.html", 
		"Resource=0", 
		"RecContentType=text/html", 
		"Referer=https://www.tangerine.ca/en/personal", 
		"Snapshot=t27.inf", 
		"Mode=HTML", 
		LAST);

	web_revert_auto_header("sec-ch-ua");

	web_revert_auto_header("sec-ch-ua-mobile");

	web_revert_auto_header("sec-ch-ua-platform");

	web_add_auto_header("Sec-Fetch-Site", 
		"none");

	web_add_auto_header("Sec-Fetch-Mode", 
		"no-cors");

	web_url("7226894891057262654", 
		"URL=https://edge.microsoft.com/autofillservice/core/page/-7241988981020077934/7226894891057262654", 
		"Resource=0", 
		"RecContentType=application/json", 
		"Referer=", 
		"Snapshot=t28.inf", 
		"Mode=HTML", 
		LAST);

	web_add_auto_header("CSRF-Token",
		"{CorrelationParameter}");

	web_add_auto_header("Origin", 
		"https://www.tangerine.ca");

	web_add_auto_header("Sec-Fetch-Mode", 
		"cors");

	web_add_auto_header("Sec-Fetch-Site", 
		"same-origin");

	web_add_auto_header("sec-ch-ua", 
		"\"Not-A.Brand\";v=\"99\", \"Microsoft Edge\";v=\"157\", \"Chromium\";v=\"157\"");

	web_add_auto_header("sec-ch-ua-mobile", 
		"?0");

	web_add_auto_header("sec-ch-ua-platform", 
		"\"Windows\"");

	web_custom_request("4MwpSUxM_2", 
		"URL=https://www.tangerine.ca/XzdnU1ENiZ-tP/yP2ljgJg/3OjS5E/YD5zScrwS8QpJc/MzF7RW8hCA/Oj9/4MwpSUxM", 
		"Method=POST", 
		"Resource=0", 
		"RecContentType=application/json", 
		"Referer=https://www.tangerine.ca/en/personal", 
		"Snapshot=t29.inf", 
		"Mode=HTML", 
		"EncType=text/plain;charset=UTF-8", 
		"Body={\"sensor_data\":\"3;0;1;0;4405057;+42GUhFh6owSFeuhdnWqmVpUMPcVF8nRj8KyP7mzv+I=;16,39,0,2,8,25601;\\\"V|u- z7m\\\"S&-\\\"lh)}7\\\"gxpH{](\\\"2;]{Mi4l[TW\\\"U\\\":~;t\\\"=\\\"l]Kd+,<h\\\"[\\\"h]>`9Q)\\\"$\\\" U14\\\"f\\\"PE?h\\\"HpKua`c@;@Ig#}\\\"vVd36\\\"|\\\"OmAu\\\"7)a\\\")m=\\\"8\\\"H;MO*@~\\\"B\\\"0oJS\\\">\\\",CxA4{wa\\\"(#A\\\"}!)\\\"C*^o[H\\\"KFr?\\\"d\\\"7Mb<\\\"^\\\"87D*\\\"R27XA\\\"+2y\\\"S\\\";C&X+>RO1]rV(+?\\\"c\\\"Dh:!\\\"l\\\">b|J\\\"g\\\"+ul<\\\"4\\\"HChpg;K;D4?CA\\\"e\\\""
		"3EMg\\\"j5,hcB)jB\\\"rkq%y\\\"P\\\"MkTo\\\"TO/\\\"wj\\\"hLJ\\\"nK_\\\"].rCW\\\"Ku\\\"jFIFX\\\"dV\\\" n6U]V<I$ygXjFT+8>f=z]G+d2-MOeu\\\"-\\\"Gu0\\\"0\\\"),7\\\"(\\\"ca]&\\\"mkLXf**8*Q^t]A@Z;Q}\\\"XS@]:\\\"p\\\"K^=w\\\"D~ZOZm|5Tq\\\"5~-\\\"u\\\"3\\\"<H(\\\"!0F\\\"mZ;cx$8\\\"RIsPRw@Krl,c{yy~YTQ2}<9.A +R0+1[/teLEJ?7}\\\"*&c\\\";!^\\\"9\\\"Nr\\\"|/(\\\"?l$(`\\\"R\\\"7\\\"2\\\"ydy+\\\"w\\\"n%myy=Vr\\\"X\\\"T.8Ywok\\\"h&L\\\"3j<\\\"TY\\\"=q5\\\"g{v\\\",Gj%:N{}F\\\"[H\\\"S1Z7iBlF\\\"xu_\\\"5-n\\\"};_\\\""
		"!\\\"`KH4a;:c,<}<:@7bCo@=EL,O[z1a&A=!<yu#Gy=@Yzw{wI4TQn{D`R.=AXpKd@$]#D=*a(8GjN^WF57&aTJghP*Za8H}R7S6UoIlX._Z^. WR?<f#rB#?{ks}M{Q+\\\"4\\\"+n&3\\\"n\\\"VG}wh\\\"ehB\\\"a<Y\\\"0\\\"*>c.{H\\\"n\\\"qU{.\\\"o\\\"CwUQ\\\">\\\"~/.f\\\"f\\\"y] >rC0\\\"a\\\"vEx8\\\"m^p<w\\\"I|5\\\"k\\\"\\\"-\\\"uEJ\\\"-\\\"xH5{\\\"[\\\"_Ck\\\"Mt@aW4`\\\"Rd&t\\\"e\\\"wBK\\\"e\\\"YA:$\\\"{_J-P[ub\\\"X>(\\\"Wfi\\\"^b\\\"!\\\"QXc+Kc\\\"3\\\" \\\"G@u\\\"B\\\"E!J96BNjr# H-\\\"G7#\\\"R%fXW\\\"$\\\"y[L~I\\\"e\\\"R{f%\\\"Y\\\"uz64"
		"=mDOc:phTVNpSdI?}RkvZ-C=YS29b~0-0eXa S3. *&@/Q<I~Vl|eMNY|0PnHOxr0oYn!b<F=XQ|e x$jHe~dUiZ1A(=o(^SoL?a}nOR^ri85YS^B3MneThhA^:]:H%#M0&Zx_KOQz#Xf{ :ud*]LD^y6aItNjRUstn/RC6GUo/Mm.8L=:i77{AX3]?uNzXg90-[ ,#@Lt!Ur5D^`[4Sc^(B|R:zb,^{JBM*aZ_i&RrOiGLgof?t!|R|Y1}QH&l2MabA| z9a0[4R3Tcr}Y43IsD4`[>1na$UdoG.EBb}g+wIm9[gsY6VZ-TO2.|jS<uV\\\"n\\\"r-!\\\"V&S>xNt/NY\\\"$}Jz\\\"v\\\"U;8,!X,5`I8Qh:^6pcC$O-\\\"D\\\"c~G\\\"}vegSRK6\\\"8g+m\\\"O\\\"iGHHB\\\"B\\\";`0y\\\"4\\\"7okhkjtmfR3O&go&B1ST;\\\"c\\\"uBz\\\"P\\\""
		"v6#l\\\"`\\\"P*u%\\\"b}<\\\"#Bu\\\"Z\\\".)fa:+Kw\\\"ZD`\\\"~3,I:\\\",\\\"za5fio;[H-.kz\\\"^\\\"p6e\\\"D\\\"37\\\"!07\\\"WL`X\\\"L|65ay}T\\\".KQ\\\"H*X0\\\"!l9\\\"]\\\"0fqM _]hG((J~OJ)58E\\\"\\\".\\\"/jr\\\"8?V\\\"ct2Jl\\\"p\\\"l\\\"u33\\\"LC%\\\"[\\\"<cCKK~4M\\\"_)+@\\\"1Be\\\"%#|\\\"*{\\\"y?S\\\"!Sjk6u;\\\"I|C(\\\"&\\\"Pk4Q-jGS`SGc)F(Yo%,JWW4T7Je.hM}-M`ZG):ak-xQ1_qVlr):YS{IUK)YX@ 7HyX^I$J Qi%>x6$oPPz/Qo)7D<+#beLz3,]>nNySVHWcZ*&~0<W~Jc\\\"4\\\"/N{M\\\"SB]I$]O\\\"]Ro4\\\"C\\\"`|r<O,@c6kF&(!\\\"V\\"
		"\"Wk:)H:v\\\"j\\\"&up!`9>5k,}kLi\\\"z\\\"4(vIQ^8\\\"k\\\"LRAwp!|OyPZ`jU;x, g\\\"c\\\"s=,h\\\"-a\\\"r\\\"<72y\\\"B\\\"\\\"+\\\"9?\\\"S\\\"/$o\\\"p\\\"Lz&n\\\"r}]|&jz50+eNxCPJ<k~KvY\\\"U|!\\\"9\\\"[\\\".P`\\\"efZ\\\"z\\\"_`>#\\\"I\\\"g-E\\\"xc3{X?\\\"BBfbGuD\\\"&\\\"kvIJ\\\"h\\\"|Ty|\\\":E,Dz5\\\"fN7u,L<At/}deSlfqnq]Ol8?8c fD9yygg\\\"{\\\"I=Q\\\"g\\\"5A=SRim#dV+TWQ)^\\\"q\\\"5I&\\\">\\\"Fwo{L rjsw5\\\"EZ]\\\":cL\\\"y\\\"oVDE\\\"9\\\"w~vE\\\"$~b><)!DV\\\"~~6\\\"V\\\"vCU [OK}8<cdIn]CLVRE$!,m@wDFdW!|/"
		"8o?~=OgPw.\\\"{-R\\\"CC?\\\"Q\\\"DW%5si6BK3t,M0\\\"~\\\"k6GK\\\"Y\\\"\\\"s2G\\\"gq%\\\")LkHYk$-\\\"8n+\\\"z\\\"\\\"$bQ\\\"g_Z\\\"]\\\"\\\"}\\\"[`.\\\"Z\\\"pD~CjCOEVH&\\\"Y\\\"t5ApfoW\\\"=\\\"/{FS1@|\\\"F\\\"~ R\\\"e~?i4\\\"wK[\\\"c\\\"-7/(\\\"t\\\"U8P)\\\"<\\\"pM9}8\\\"l\\\"VfXt\\\"R\\\"=Q\\\"!\\\"o-c8\\\":\\\"lK!k\\\"}\\\"tNv}\\\"^\\\"*\\\"5\\\"h7x.\\\"v_\\\".8\\\"7Bs4\\\",&M@\\\"J5\\\"Nr]/\\\"5\\\"zerYq.D,[c/z<C?*w873K]A51$P}`gsMr_ck(n$OdmM(/ZV7mSa`k<-Iku#>F-|Ki14QI%D-.Q fx\\\"h\\\"x%-g\\\"R\\\""
		"zWo-sZ%!^*g?9\\\";7:\\\"K_Kb\\\"o;$\\\"[b`\\\"`5h4>\\\"#8B\\\"wb:+fVubn./q8O:ioR\\\"KRO\\\"O\\\"Mxtc\\\";\\\"3C$!\\\"`\\\"asH6;] hRSM_]hak\\\"8\\\"nje\\\"s\\\"%~ec\\\"9\\\"C#LN\\\"(\\\"n,$&6=V<]-\\\"2k~\\\"p2 ^\\\">F.0\\\"N\\\"3FQ)\\\"Z\\\"E\\\"Rrw\\\"0qb\\\"B\\\"E\\\"B\\\"^weq\\\"n\\\"OIs/-Y,]y@Tj|CL\\\"r\\\"%};:\\\"Q\\\"9j_odgLoofy}^@C\\\"l\\\".[,/\\\"H\\\"`x\\\"NN vio,h)/C.wnIgE1G\\\"u\\\"3qAI\\\"v\\\"|(JS8ma)DAWO_19}`&F,$boZ&ZlCdsKsiz2O|b|!$%i=_NN/~:LOO|,T{MfJS)[laIprX$26U|h6NNjkP5#~x101L1g;"
		"R4EQU;7caOqfYp4Rkm*i#g4XOp,f,k4yK\\\" XC\\\"]&,\\\"U\\\"/Ah4cbrlf?gup\\\"6#?\\\"V/s\\\"1M>Gq\\\"<3YU\\\"k\\\"\\\"*\\\"5/C\\\"o\\\"p\\\"[\\\"T[H6\\\"Ka%+-\\\"3D5d\\\"s\\\"Ae,h:14t_gi*cO,mI-WG-e{(UGUOe5x.\\\"C\\\"z7Pc\\\"HL^\\\"1(p\\\"vf6+L\\\"vC!\\\"B.\\\"pt@(\\\"?\\\"-3\\\"yp|\\\"d|qi\\\" kO\\\"g/A\\\"|\\\"?^5~n\\\"*\\\",kIY\\\"c\\\"Z\\\"G.{\\\"_ON\\\"c\\\"/j8oh,10iJ,rIgC33[WN~kLbkVf_hG#e[FikCU8g-&w?-kDo5W9Q/]R;E1JE;B^=GY$]P_&iATbv^R:=H:Z`*VBTXYtr.$3qm!5=<qA+(0gr_XCw]SVwR/*iy|=2V\\\"e\\\"7{c]\\\"?"
		"\\\"\\\".3s\\\"Tt<\\\":^^U{T)\\\"NFWF>V{sQhi5pe\\\"U\\\"2*2\\\"U\\\"=>uu8pc-LX)Q_M%E)>5!zv]Zj +x8+Rn0War%5:D0Y$\\\"[A<\\\"X^5\\\"c\\\"shul{s98\\\"b\\\"+`}=zi!\\\"v\\\"Rj<V!\\\")\\\"P+B8\\\"%\\\"%/Tl;9!2>>b5vC_|8t(p(FckHCq*d=*n9yV$ gJA6aM4\\\",\\\"JzU\\\" \\\"3gz0AI/S.NC\\\"=\\\"lx,I$,G\\\"=79a(\\\"wAW\\\"X\\\"0\\\"rLi\\\"Mal\\\"q\\\"o_gzrdQWvdXhO9M{b.,\\\"i\\\"SM-$\\\"=u\\\"l?~w#\\\"t\\\"(m\\\"c_\\\"B-#^\\\"~\\\"V7y*oqHI_we7ZtRl\\\"O\\\"oM]\\\"^\\\"Z0.r\\\"0\\\"*($1\\\"VcZ\\\"%d}\\\"X0Gk\\\"lgH"
		"[\\\"F\\\"R-+eeqrNo2J$|Xpa-n;(Z*+hoP2)w,!L3s5NT5 80:8D9g#V#T-+91#Lgqh6CA.[SNy44)$pN)voQm}|S<se8/R/KVt!K`T*GFL<A;:joM~5)Rq>pkHA~\\\"B\\\" ^bQ\\\"J\\\"t\\\"g\\\"W } \\\"Xt4mhm\\\"wp`NV4)XUtd)+S\\\"1\\\"lS#},(;\\\"E\\\"PieF<\\\"4=#\\\"aZ9yt\\\"IAwE\\\"l7;S\\\"&{#i&c5z&Y}tKF[%*#UQxgGg9pjU$mS4gp(@\\\"s\\\";hCu\\\"P\\\"PeGZ@1\\\"8\\\"B>vx\\\":5`n=DTXH\\\"Oz\\\"/WM?X0WD\\\"3}c\\\"x]Y\\\")8Ia*\\\"B\\\"sn{\\\",+b\\\"i.,=\\\"NKf_[z{(\\\"rXl\\\"ah<\\\"q{ME\\\"x_l7u_mIke\\\"y9)3\\\");\\\"M\\\"8S J\\\"J\\\""
		"7\\\"g\\\"S`(E\\\"%\\\"%CO\\\"u\\\"xF5*\\\"n4\\\";SI6q\\\"S\\\"}0\\\"6W\\\"2=4<\\\"g\\\"?Xx!3&n:ne[ 7e5rB0V~=`IR!UH1AT}1dyQGlYS*_S]y1k?&R8fRj31(m\\\"3\\\"$?l\\\"+\\\"\\\"a/|\\\"D{1\\\"!\\\"5 !ek0$|0>D\\\" \\\"f|>m e$\\\";jad#pt\\\"@WI\\\"?\\\"_F!#~%CNd_8bMTwUO`KwO eEW5Fg^7)wow-i5v`EQjC<Viit%;ZK+qwmI0srdGn/\\\"1)R\\\"4M>\\\"]d*]7\\\"CnS\\\"$t6 \\\"p.y<\\\"Yw)\\\"aZF \\\"!\\\"5!`90O`w\\\"e\\\"J!92\\\"J\\\"B\\\"lmo\\\"YG7\\\":\\\"!3{DQf=XPU#urJ,nlO(_z32D%q-|(YW(VcKzE}ZRH7 h4I#RQB~chHJ0?;="
		"rKe@Z-yZH6zYuOa30m\\\"#\\\"<Y*P\\\"E\\\"o?S[`yp\\\"P\\\"n1a8\\\"g\\\"k9$)of/[o}vml]\\\"D\\\"an|4%{V\\\"k\\\"GkjI\\\"B\\\":RH;\\\"E\\\"W7}w\\\"|\\\";f:;\\\"X\\\"g} DMKE7\\\"3\\\"!./s\\\"c=KE$xB\\\"SJ`&\\\"k*S\\\"uw1\\\"|\\\"i)&-5@?A#_|8$\\\"et&\\\"Wx<cy\\\"qw{\\\">;ksp\\\"W\\\"!U:S*LwNiXfpZfqW0Bn5r5&p`3*-0Di7Kq[t_OxED$7>nPL(UnZ$T% 7]F{m7*5ERd>{C8JC0*;Oz\\\"$P\\\"Fu\\\"!d_rJ/S\\\"0z.uB]y_?Nu\\\"k\\\"q%c4wO4\\\"lKF7?oLF>UpaP\\\"1CP\\\"J9k\\\"1>V\\\"|\\\"?\\\"]\\\"`:cj\\\"Q~ j^vYF,Py<QQpgadU6UPdl;"
		"FfN.OpQL2&T\\\"5\\\"yvE!\\\"o\\\".5y!1_?]YKVD/@3dcz{\\\"q\\\":oQ!\\\">\\\"/^dqiKZ\\\"C\\\"RNQI\\\".xEj.5\\\"[j2S\\\".\\\"M~\\\"{\\\"J~kQ\\\":M+mUw\\\"Vf`4\\\"9\\\"?\\\"F\\\"tSA+\\\"T\\\"%w#ay3]*{Q<=C8J#?rf\\\"A<%L`Cmg>8r\\\"}py\\\"1sU\\\"x\\\"35^y4\\\"S>{\\\"XHR\\\"g\\\"[t]\\\"1~W@c\\\"(\\\"3!qS\\\"`\\\"\\\"{\\\"aUP\\\"a^G$;\\\"XNA\\\"O\\\"$`8]\\\"L2\\\"5HVS\\\"!,7(#i\\\"nu<\\\"@\\\"kjMc\\\"?\\\"aI *\\\"n\\\"\\\"p9-\\\"I`|\\\"N<sRWk>R_2\\\"y}$7\\\"9U.CE-bnSa+NT%wF\\\"*n?\\\",\\\"D4 //B7H:,dBU]K2."
		":L^\\\"8\\\"Vzo\\\"3\\\"lp\\\"T\\\"(W]v\\\"+pv[<HeM=O\\\"m\\\"7vSa\\\"5]m\\\"W~UNC\\\".w\\\"~>7\\\"F\\\"MeZ?T[\\\"F\\\"|y?X\\\"#\\\"`\\\"9\\\"P{%=\\\"o\\\"0\\\":\\\"X7fU\\\"_^%Kz\\\"}-pu\\\"RAg7!`{k\\\"0Yu/\\\"n_U~?C:Qi?^CjV&Vjmr[\\\"K:C\\\"!s=j|EOmj_2y+\\\";V!M5n_\\\"`\\\"0r \\\"U\\\"A]g\\\"K\\\"/}!R\\\"FkHF\\\"Y.{S\\\"xc1v8RWY\\\"[O\\\"GO#\\\"X}K\\\"P\\\"N6pjyBpX6#TX3\\\",\\\"Vuf4\\\"H\\\"G9_h4\\\"}\\\"7VB}\\\"GW\\\"m[b;\\\"y\\\"\\\"`\\\"laSg\\\"4\\\"9`J{!H{USJ)|+o)NtjSJg.[89-mSm&2V;d~J1].?[t])."
		":?8(;qI-~\\\"1\\\"GM%\\\"/\\\"+uG\\\"U w\\\"V1)v\\\"Y\\\"Hp]oh4,R2qia*Gex[+I[V2!U,@n`2 H1pGl}pzlt)vs:g~[nS/JY(<?i]:7e3^[z\\\"V4]~\\\"%2\\\"i\\\"CYh/\\\"I\\\"j\\\"I<3\\\"Oe4\\\"b\\\"XL>G\\\"f\\\"i):,\\\"T\\\"*4h\\\"eVA\\\"|~kdD\\\"s\\\"xL3+\\\",\\\"4V{!\\\"1)Wl?Z\\\"*vc{a\\\"-\\\"Yp>*\\\">\\\"LJH^\\\"%\\\"Bo0z\\\"n\\\"]xU6 JYsQQOJd/7hyW@^%|$sWn9MAE:7Hk2&*q%9^CYE9>;esZDz)DIw(WULya/q35MZ/~0dj}*%v\\\"H\\\"rrjs\\\"Ri9c8Lw0<ko|\\\"{l~d\\\"^}1>\\\"37#R\\\"q\\\"q!CmB\\\"C\\\"+In]\\\"(\\\"3!8\\\"8]w\\\""
		"8LF90\\\"O\\\"G3HxG|R4\\\"I\\\"uXf5UH8\\\" uC\\\"}LO\\\"/I\\\" N\\\"5A&H\\\"TAY=\\\"i5\\\"NB;;\\\"p\\\"C Flz6.([=?Eh\\\"We)\\\",!^$\\\"PO)J^f6\\\"\\\"!\\\"cU|;\\\"B\\\"\\\"B++\\\"ss\\\"G\\\"vQ\\\"=FE\\\"I_Y-2\\\"\"}", 
		LAST);

	web_add_cookie("_abck=8DA07508E26DC426BD75C52455AB998D~-1~YAAQD5YqF+yHXcOhAQAA7VYKzRBeXr3G9HkK2KK4wAJqwSt2tZvOT7K02pYdRvPohGvYBb+ZJ5zNnpRLvMJt02A5kvmaiZC+SmRtbvWTeQ49eF7DTW/dK9+MsMPZSTImVfHNuEdLmdLIGDQyAgv9jOXeBN5HaMzgAJ4HCUzQjOOPJruOw8KAX2tZNSi33B7K/ANkc+JmZawpk8AqRhd/dHEwbOO7MSw8u8N1RfgH6trblmJWDW2gyASntuiauHlJLnu6vGmD3NzxTtCXK0WSJhPDCD/+tENwZyC3zBvNJI1n08ACME7fD1hKcml/Ipvi/VevAzl9cHNBwuimntJmDzrBduR6wnsOUfqbC7UqYkfwA0BsgXh7g/3sNcyFnBMsVxaejxBRgdWSlkVDEEgyFE1WtFVv0BAdIbeJ8RgcEbMfAB4e8eF+"
		"j5pyLLrzwtsFH93MJJHfbDInS1mQWi5cfm9NXJ2s6th9/OaYzFZyfRz5OPjDr8za19F3N7stcF+gXAxvzego7NVtyM9ncNp2mlVd4vv3Mrk25Z8kVBYipNbNlpCankl1GLhzvheDen+EiV9Pzt7kzTfH/6+8yKy4fAwPyYJMr0H2~-1~-1~-1~AAQAAAAG%2f%2f%2f%2f%2f+fG3r0MTcVVm3vsP8Qdln0K138Bx+r5Ci8eeo%2fP1PwlscTcBraMZBQyZsBkAnhfE86wHB0kmnp7zSgTu6d9p3M6fEoAjm1mUcok~-1; DOMAIN=www.tangerine.ca");

	web_custom_request("4MwpSUxM_3",
		"URL=https://www.tangerine.ca/XzdnU1ENiZ-tP/yP2ljgJg/3OjS5E/YD5zScrwS8QpJc/MzF7RW8hCA/Oj9/4MwpSUxM",
		"Method=POST",
		"Resource=0",
		"RecContentType=application/json",
		"Referer=https://www.tangerine.ca/en/personal",
		"Snapshot=t30.inf",
		"Mode=HTML",
		"EncType=text/plain;charset=UTF-8",
		"Body={\"sensor_data\":\"3;0;1;0;4405057;+42GUhFh6owSFeuhdnWqmVpUMPcVF8nRj8KyP7mzv+I=;10,39,0,0,4,25601;\\\"V|u- z7m\\\"S&-\\\"lh)}7\\\"gxpH{](\\\"2;]{Mi4l[TW\\\"U\\\":~;t\\\"=\\\"l]Kd+,<h\\\"[\\\"h]>`9Q)\\\"$\\\" U14\\\"f\\\"PE?h\\\"HpKua`c@;@Ig#}\\\"vVd36\\\"|\\\"OmAu\\\"7)a\\\")m=\\\"8\\\"H;MO*@~\\\"B\\\"0oJS\\\">\\\",CxA4{wa\\\"(#A\\\"}!)\\\"C*^o[H\\\"KFr?\\\"d\\\"7Mb<\\\"^\\\"87D*\\\"R27XA\\\"+2y\\\"S\\\";C&X+>RO1]rV(+?\\\"c\\\"Dh:!\\\"l\\\">b|J\\\"g\\\"+ul<\\\"4\\\"HChpg;K;D4?CA\\\"e\\\"3EMg\\\"j2*gj@)jB\\\"rkq%y\\\"P\\\"MkTo\\\"TO/\\\"wj\\\"hLJ\\\"nK_\\\"].rCW\\\"Ku\\\"jFIFX\\\"dV\\\" n6U]V<I$ygXjFT+8>f=z]G+d2-MOeu\\\"-\\\"Gu0\\\"0\\\"),7\\\"(\\\"ca]&\\\"mkLXf**8*Q^t]A@Z;Q}\\\"XS@]:\\\"p\\\"K^=w\\\"D~ZOZm|5Tq\\\"5~-\\\"u\\\"3\\\"<H(\\\"!0F\\\"mZ;cx$8\\\"RvsPRw@xrlXd}h*mAL> };9.A +R0+1[/teLEJ?7}\\\"*&c\\\";!^\\\"9\\\"Nr\\\"|/(\\\"?l$(`\\\"R\\\"7\\\"2\\\"ydy+\\\"w\\\"n%myy=Vr\\\"X\\\"T.8Ywok\\\"h&L\\\"3j<\\\"TY\\\"=q5\\\"g{v\\\",Gj%:N{}F\\\"[H\\\"S1Z7iBlF\\\"xu_\\\"5-n\\\"};_\\\"!\\\"`KH4a;:c,<}<:@7bCo@="
		"EL,O[z1a&A=!<yu#Gy=@Yzw{wI4TQn{D`R.=AXpKd@$]#D=*a(8GjN^WF57&aTJghP*Za8H}R7S6UoIlX._Z^. WR?<f#rB#?{ks}M{Q+\\\"4\\\"+n&3\\\"n\\\"VG}wh\\\"ehB\\\"a<Y\\\"0\\\"*>c.{H\\\"n\\\"qU{.\\\"o\\\"CwUQ\\\">\\\"~/.f\\\"f\\\"y] >rC0\\\"a\\\"vEx8\\\"m^p<w\\\"I|5\\\"k\\\"\\\"-\\\"uEJ\\\"-\\\"xI5|\\\"[\\\"_Ck\\\"Mt@aW4`\\\"Rd&t\\\"e\\\"wBK\\\"e\\\"YA:$\\\"{_J-P[ub\\\"X>(\\\"Wfi\\\"^b\\\"!\\\"QXc+Kc\\\"3\\\" \\\"G@u\\\"B\\\"E!J96BNjr# H-\\\"G7#\\\"R%fXW\\\"$\\\"y[L~I\\\"e\\\"R{f%\\\"Y\\\"uz64=mDOc:phTVNpSdI?}RkvZ-C=YS29b~0-0eXa S3. *&@/Q<I~Vl|eMNY|0PnHOxr0oYn!b<F=XQ|e x$jHe~dUiZ1A(=o(^SoL?a}nOR^ri85YS^B3MneThhA^:]:H%#M0&Zx_KOQz#Xf{ :ud*]LD^y6aItNjRUstn/RC6GUo/Mm.8L=:i77{AX3]?uNzXg90-[ ,#@Lt!Ur5D^`[4Sc^(B|R:zb,^{JBM*aZ_i&RrOiGLgof?t!|R|Y1}QH&l2MabA| z9a0[4R3Tcr}Y43IsD4`[>1na$UdoG.EBb}g+wIm9[gsY6VZ-TO2.|jS<uVQyL?GN!P)U5qKsGNuSEScFvmPW@93}N-<`T3Ue?i;uc=vL);PH+FjHzmkkQnQHxc%E2,Ng0hN$%IO|Wk\\\"r\\\"^5l\\\"xmxj#vm@.=\\\"QDl~\\\"b\\\"1(jX3t=QGHp:#nu\\\"l\\\"[Mc\\\"b$C@@Z+a\\\"ybfF\\\"F\\\"$Wh3l\\\"Y\\\"4Xlg\\\",\\\"za2kes7`C3/o$[dB0g"
		"|+E\\\"2\\\"khz\\\"_\\\"v-wy\\\"w\\\"vc/$\\\"vSZ\\\"@ss\\\">\\\"X/^SP]d1\\\"K]k\\\"J+Wt|\\\"W\\\"7007962{Y)=H.\\\"e\\\"qgC\\\"B\\\"c^\\\"3#$\\\"d?11\\\"[np$lZ=i\\\",yz\\\"27T!\\\"<h}\\\"Q\\\"Ge~$)PAh|:~R@A(U}F2\\\"\\\")\\\"Cq7\\\"L:a\\\"FBPu[\\\"r\\\"&\\\":HS\\\"_<|\\\"-\\\"8Y^5xLgB\\\"oCXL\\\"`xn\\\"HQ`\\\"^O\\\"tri\\\"G5  AB@\\\",rTm\\\"c\\\"ub6F=b-0Kg=TzUk.:^//&* f8Ak[h8k7z{mibUgd1Rh>|7]LUuLZ;bG%dEpEi1Enr+!wvz9g8re4Zn(ML0b`o4UAmJ[Z8pKu<C#ZZ`-,}kL3g%HIP2dt|\\\"s\\\"x5ud\\\">#^r~RX\\\"W<`5\\\"M\\\"hB[r|hFKgRHL,.\\\"+\\\"VmWYhb>\\\",\\\"#}OMqYv?aq!4AT\\\"0\\\"PGC:~qJ\\\"g\\\"s8IM-LOBV~6N&g<2s3k\\\"(\\\"Zqwu\\\"f6\\\")\\\"%8Sd\\\"x\\\"\\\"*\\\"-R\\\"q\\\"l|?\\\"6\\\"jj l\\\"rlC#Sy&Bi+cC|o_T85|(I<\\\"Rdk\\\"s\\\"k\\\"dic\\\"*M~\\\"F\\\"$nO@\\\"x\\\"/id\\\"tmm&X>\\\"+s-3<H[\\\"e\\\"US2V\\\":\\\"S[kP\\\">tAXH!\\\"~rnzu7?R`kVP}cjk8mR:?*:00zr:qyw^;A\\\"/\\\"H?!\\\"Y\\\"NrbbtH!%]`ZgerT`\\\"X\\\"S:p\\\"H\\\"c-4hi)|2_Qe\\\"=$o\\\"kZ \\\"D\\\"4eTa\\\"V\\\"-<cz\\\"h*9Zak738\\\"1mi\\\"2\\\"[,I)1iuO:v .7x]2B|R)p#XpB!nIY"
		"H&N6-{kts3Nc`c\\\"yRZ\\\"Y(G\\\"P\\\", HZV#L?hw=>rp\\\"s\\\"vYLK\\\"x\\\"\\\"-i8\\\"$ P\\\"e OD84>b\\\" >i\\\"C\\\"\\\"DGs\\\"~0[\\\"<\\\"\\\"i\\\"=HG\\\"P\\\"&7XyYcI2Nen\\\")\\\"zdr>G/[\\\"H\\\"3b8XbW5\\\"%\\\"x(k\\\" *O;/\\\"_6r\\\"O\\\"?qK?\\\"^\\\"a:rr\\\"c\\\"hiS1j\\\"9\\\" Ls}\\\"b\\\"FU\\\"E\\\"FX@-\\\"Y\\\"LOsE\\\"0\\\"A|b}\\\"2\\\"$\\\"K\\\".1@J\\\"]d\\\"~6\\\"7)X~\\\"3~Si\\\"8 \\\"r!M+\\\"!\\\"N?|>H^:Ndj=JD?53NdQT@xO>Mmp=&=#>^_0[ue;07+|rOjn]m%.@gm;_BtRi%uMHmTp_Q1k*h#q d\\\"A\\\"3zxd\\\"I\\\"NG$|[S$bwF1=c\\\"Z~S\\\"Caqf\\\"X<V\\\"Yk/\\\"c%p[P\\\"#]4\\\"NPX$A= *-9BUT_D)Z$\\\"q:o\\\"^\\\"<=(.\\\"N\\\"3FS(\\\"Z\\\"EJhy-4E5/W5@AhG@\\\"r\\\"SJH\\\"H\\\">HV&\\\"Y\\\"Dq3D\\\"u\\\"KrA 9> 72s\\\"Zak\\\"%uP1\\\"@&cd\\\"l\\\".].1\\\"H\\\"-\\\"e3Z\\\"%fn\\\"X\\\"Y\\\"8\\\":j*n\\\"X\\\"-j$Usz@k=@+?X@p\\\"%\\\")Wag\\\"h\\\"=$4+lv{hJ<R$9hc\\\"&\\\"qD0x\\\")\\\"gb\\\"6QX>(=!0IR$CliC+9m9\\\"8\\\"9vnH\\\"c\\\"J2KTOgE^&G<+I!k,`A&8(dxGJq0+*~T6K7Ox[l}p,Lk1Ma?SDf9&g1bXU&VJ.CrGh&LUKP?>qU(Cb#gJ+!.nFd$ML+dSQowFa9}_x-=9,jnw"
		"6cCapujaBf=-?vM]N\\\"!et\\\"b+W\\\"?\\\"s[iu9cQ+x_J$|5\\\"e(Q\\\"9/]\\\"|5jCg\\\"FGe2\\\"V\\\"\\\"T\\\"m[Q\\\"P\\\"_\\\"A\\\".&?C\\\"7s*{F\\\";sv$\\\"~\\\"!X{3)zglTV|Km/wTdg.Od84^8lKOZYJS\\\"S\\\"rJjL\\\"cX&\\\"a#r\\\"W^~`:\\\"S7w\\\"]J\\\"Sj5R\\\"z\\\"Si\\\"LQG\\\"`s=B\\\"u2_\\\"y;3\\\"9\\\"o9d~x\\\"Y\\\"{>7M\\\"S\\\"B\\\"p8S\\\">j \\\"t\\\"h!uP7!*%(yHic}35CUuj$44!pjb@hAPdDqea/pM#vjcjcIPHrfr4OZV~fXd;WPYOLL=*X@i;9_YWQEd+DmRfxic_HW]0gW;J@:j|qVAo=_>xoo,zu=kD`Vg:u1ArO\\\"<\\\"&YWc\\\"Y\\\"\\\"p*g\\\"4AP\\\"_lA7FC%\\\"wmxLSfo(^YzP!6\\\"&\\\"=+q\\\"G\\\"<3Ju.WuFW@&1,~YU`gK`]6RcO>YH>Ci^Bi[~@9a,`_7\\\"=17\\\"FUp\\\"i\\\"~/2Gq`em\\\"n\\\"WoY|Mgt\\\":\\\"{pXum\\\"=\\\"iEJh\\\"T\\\"077a-rn{q7ir+di]&[BKZN=/_xRNY>m$x@LF9_]Y}(i@\\\"i\\\"F0k\\\"w\\\"hT{[5Op^KY&\\\"1\\\"KVApY:+\\\"g$EF@\\\"KHl\\\"L\\\"<\\\"5wy\\\"9C}\\\"#\\\"kP;ifIQM_w#r&&-I6a<\\\"D\\\"4/Ix\\\"35\\\"+E90q\\\"&\\\"D*\\\"=7\\\"F?0?\\\"y\\\"D|V&v]cnyc[#(K}x\\\"}\\\"J/0\\\"c\\\"{gVh\\\"O\\\"<,&I\\\"p4>\\\".~)\\\"] !X\\\"B_NK\\\"g\\\"C+p @G.uBH tDOpVQOq/{@pz*;"
		"GC%c`{@(90L|G7}u<J-$AaeJ~Fwl(%>2<vl?*Qm)L:H7v%[+),bNYMSV%F5 %z?,tw3r}4/5=g$nJ3Ke^tUHz5?<uG9\\\"3\\\"2W~|\\\"#\\\"E\\\"y\\\": w_\\\"PR@sSw\\\"5]UJqydv}S$bj(\\\"5\\\"?-L&IF&\\\"Y\\\"j6mu}\\\"=X,\\\"T]rh`\\\"AGgX\\\")t9K\\\"aQ<BWy{]KO}j`)#y::Me4a[4EIJ(~2Ws_k].\\\"@\\\"B]^4\\\"D\\\"5 &(Th\\\"W\\\"#gt&\\\"dl3temIke\\\"p7\\\"_3|?cA:@\\\"d{V\\\"ycQ\\\"QR2_w\\\"%\\\"&HV\\\"ij1\\\"r#Hl\\\"Ue|Nn=eE\\\")2S\\\"f{H\\\"qu-4\\\"E[u|1,r$aP\\\"bu5j\\\"G&\\\"~\\\"<IR$\\\"P\\\"E\\\"y\\\"FxRM\\\"h\\\".^W\\\"y\\\"TD1]\\\"t$\\\"ln)4Y\\\"/\\\"8g\\\"M/\\\"V343\\\"H\\\"EyAyF?h_;r6_fqG)$)PU+O(G)9c^[9t$1X|[F1rZ@|Kv&6vWX^(F|?!I+\\\"r\\\"S?*\\\"j\\\"\\\"D.q\\\"D#v\\\"<\\\"z}`2Nd5EiT#\\\"O\\\"nrZNOkM\\\";|r_P=x\\\"(:_\\\"K\\\"_Aa va?TPz]|)Jd#7=hP|AA&+3J] nb}.8*|Yxxpj<(k_%qgx-%I&F!t9R6|DFfY\\\"dA-\\\"J$}\\\"cu}#f\\\"I2k\\\"7/0F\\\"/eXk\\\"m/h\\\"Z24p\\\"&\\\"v=}D#EC4\\\"C\\\"#WWs\\\"&\\\"N\\\"7FC\\\"nU;\\\"V\\\"CM.s=HNsa7}wF9}SlUn$EMwBs/oQ833OGDx!M%+5u=:~4]D]nm5MPwNRK->mxR88:!Fck7El<.xky\\\"Q\\\"u;ZN\\\"<\\\"HxYx u$\\\"B\\\"<JBy\\\"o\\\""
		"&xv+JS,2g%v2?x\\\"B\\\"{IRM]_m\\\"L\\\">{`~\\\"x\\\"Zy@M\\\"@\\\"$CVg\\\",\\\"OWB5\\\"W\\\"Dq8(iy`+\\\"&\\\"qiCL\\\"# >n!&8\\\">{fK\\\"_=q\\\"8DQ\\\"i\\\"yC7|2C!?uD|?z\\\"0~l\\\"HE}H<\\\"M1Z\\\"k1tz/\\\"7\\\"Km;fJF6y~2MA_+~:0<M3jq!vKMNHzJTb!NiN>nS&v#K41*(/s/V7i)Kbe(o>@E=7Vfwz?kRI}M]jj\\\"j{\\\"-0\\\"S-GT 5d\\\"T]d{csq$XH<\\\"w\\\"bUoV.1<\\\"CI6rCvAakpSgE\\\"n~u\\\"!XN\\\"j<c\\\"H\\\"p\\\"#\\\"TL l\\\"|2bU/)tWlL{m?EVhg[x_p9blf*Kpf+9A._.^\\\"b\\\"X0oI\\\"#\\\"(RG7hF~b}WHD)m m@)4\\\">\\\"TZW|\\\"&\\\"K7C2D.>\\\"W\\\"%9.O\\\"Lth21^\\\"dKt6\\\"H\\\"/r\\\"W\\\"FSsh\\\"LnE]Sp\\\"B;x{\\\"P\\\"~\\\"<\\\"k,!O\\\"u\\\"/-<Z@^jbk3H`W+S.tpf\\\"FBwg/^Q^2cQ\\\"DJa\\\"re~\\\"(\\\"[l12Y\\\"Wa:\\\"ztc\\\"R\\\"l2n\\\"=!;?h\\\"(\\\"+E=o\\\"^\\\"\\\"_\\\"#/,\\\"PP(+C\\\"(0o\\\"x\\\"$$IW\\\"wF\\\"-+[v\\\"b=,f q\\\"z.9\\\"e\\\"V`J1\\\"-\\\":)Ad\\\"A\\\"\\\"vkt\\\"O/=\\\"bcov%v~G0:\\\"#p*)\\\"7QqL]z&1nQ*F o]_\\\"l&&\\\"a\\\"E:VndHX`2N|<z;Wi{ii#\\\"*\\\"Pbm\\\"o\\\"rd\\\"$\\\"y^PC\\\"g8O3Z<V*;[\\\"8\\\"y}x \\\"Gyp\\\"$A7:%\\\"H*\\\""
		"-@y\\\"J\\\"M{Sc}v\\\"D\\\"J^ry\\\"]\\\"@\\\"v\\\"iqS}\\\"u\\\"V\\\"M\\\"Rd3j\\\"W?:n9\\\"~8Os\\\"0N~!M&8V\\\"-&]j\\\"X?tj1t8g`pG|!%FR/4t&\\\"ey7\\\";@V[!G+kgE:2x\\\"[rq[-;:\\\"y\\\"a;g\\\".\\\"QR>\\\"#\\\"O6+e\\\"A3sc\\\"Im+f\\\"jk+_7RE^\\\"Ok\\\"bCw\\\"&n)\\\":\\\"mxcEwNf$nTk}Q\\\"O\\\"XH3T\\\"E\\\"WS Y1\\\"a\\\";<B7\\\"j!\\\"TkRv\\\"_\\\"\\\"<\\\"KR!]\\\";\\\"x/PFJI@v^gd4rVhc9*FJakY@(9%O*KMCAOK2lzf|z`NZ-NEiod+wK-\\\"U\\\"qx>\\\"p\\\"43`\\\"j#c\\\"Rt1/\\\"}\\\"c`Zg5~p{iT2Iz|k+b`,4]R9MOjx&]>2 RS14b$w[&vP>n%v=npPNc,z06!VH$9Y)\\\"!k@&\\\"E&\\\"(\\\"t7yo\\\"+\\\"7\\\"<H5\\\"Mix\\\"x\\\"{(i@\\\"U\\\"]l[d\\\"{\\\"yqo\\\"k%!\\\"6J4dg\\\"}\\\"Vqjp\\\"A\\\"PH.-\\\"02ExUV\\\"`3_#]\\\"s\\\")I.H\\\"1\\\"J_>1\\\"`\\\"o0,?\\\"q\\\":C7+bc&.CUR&b+zp2Hc1@l!l%Y|f+)b|:B87~Iundt!>]VE,@x/jhP|.xa`4wa{vI9x*Ys7W7me:a\\\"g\\\"dMi3\\\".Rzi^l{RX}CZ\\\"mh`t\\\" o=@\\\"2<wc\\\"i\\\"=>;kB\\\"7\\\"K3I%\\\"x\\\"9+.\\\"*=0\\\"NLik+\\\"-\\\"1x+0j;DD\\\":\\\"m6b;Rtm\\\"{{@\\\"e*l\\\"li\\\"q \\\"IGX2\\\"Zn+:\\\"07\\\",Z.0\\\"x\\\"lrKnU4:keT"
		"/h;\\\"Hd~\\\"uf)m\\\"w7x dw,\\\"\\\"h\\\"7}t^\\\"L\\\"\\\"_rx\\\"29\\\"9\\\"p9\\\">5Y\\\"M,*H%\\\"\"}",
		EXTRARES,
		"URL=https://fonts.googleapis.com/css2?family={family_3};500;700", "Referer=https://www.tangerine.ca/", ENDITEM,
		"URL=https://fonts.googleapis.com/css2?family={family_1};500;700", "Referer=https://www.tangerine.ca/", ENDITEM,
		"URL=https://fonts.googleapis.com/css2?family={family_4};1,300..800", "Referer=https://www.tangerine.ca/", ENDITEM,
		"URL=https://fonts.googleapis.com/css?family=Material+Symbols+Outlined:FILL@0..1&display=block", "Referer=https://www.tangerine.ca/", ENDITEM,
		"URL=https://fonts.googleapis.com/css2?family=Roboto_old:wght@400;500", "Referer=https://www.tangerine.ca/", ENDITEM,
		"URL=https://fonts.googleapis.com/css2?family={family_2}&display=swap", "Referer=https://www.tangerine.ca/", ENDITEM,
		"URL=https://fonts.googleapis.com/css2?family={family}&display=block", "Referer=https://www.tangerine.ca/", ENDITEM,
		"URL=https://fonts.googleapis.com/css2?family=Luminous+Symbols:opsz,wght@20..48,100..700&display=swap", "Referer=https://www.tangerine.ca/", ENDITEM,
		"URL=https://fonts.googleapis.com/css2?family=Google+Sans+Flex:opsz,slnt,wdth,wght,GRAD,ROND@6..144,-10..0,25..151,1..1000,0..100,0..100&display=swap", "Referer=https://www.tangerine.ca/", ENDITEM,
		LAST);

	web_add_cookie("OptanonAlertBoxClosed=2026-11-11T23:56:50.939Z; DOMAIN=www.tangerine.ca");

	web_add_cookie("OptanonConsent=isGpcEnabled=0&datestamp=Wed+Nov+11+2026+18%3A56%3A52+GMT-0500+(Eastern+Standard+Time)&version=202502.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0002%3A1%2CC0004%3A1; DOMAIN=www.tangerine.ca");

	web_add_cookie("_ga_RFBV4QJDD5=GS2.1.s1794441370$o1$g1$t1794441412$j60$l0$h0$dNthi1IV-i32633AXvoRz2J9h5rXyUVnVGg; DOMAIN=www.tangerine.ca");

	web_revert_auto_header("CSRF-Token");

	web_add_auto_header("Sec-Fetch-Mode", 
		"no-cors");

	web_custom_request("c_2", 
		"URL=https://www.tangerine.ca/evtservvs/ag/g/c?v=2&tid=G-RFBV4QJDD5&gtm=45g92e6ba1v878796413za20kzb9174847117zd9174847117xf4&_p=1794441323654&_gaz=1&gcs=G111&gcu=1&gcd=13r3v3r3r7l1&npa=1&dma=0&gdid=dYWJhMj.dNWVlNT&_eu=AAAAACQC&_uip=%3A%3A&cid=1478828077.1794441375&fp=1&frm=0&gcut=3&ibt=1&ngs=1&pscdl=noapi&rcb=16&sr=1920x1080&uaa=x86&uab=64&uafvl=Not-A.Brand%3B99.0.0.0%7CMicrosoft%2520Edge%3B157.0.4341.46%7CChromium%3B157.0.8103.39&uam=&uamb=0&uap=Windows&uapv=19.0.0&uaw=0&ul=en-us&ur=CA-ON&_gsid="
		"Nthi1IV-i32633AXvoRz2J9h5rXyUVnVGg&_s=2&tag_exp=115938466~115938468~118897920~118897930~120213116~120385422~120412528~120420416~120469145~120469153~121246026~121246034~123329123~124170881&dl=https%3A%2F%2Fwww.tangerine.ca%2Fen%2Fpersonal&dp=%2Fen%2Fpersonal&sid=1794441370&sct=1&seg=1&dt=Personal%20Banking%20Online%3A%20Digital%20Banking%20in%20Canada%20%7C%20Tangerine&gtb=3&_tu=CAg&en=user_engagement&gap.gtb=3&gap.gtbd=23&ep.gtm_tag_name=GA4%20-%20AEM%20-%20Configuration%20Tag%20-%20VS&"
		"ep.tracking_optin=C0001%3A1%2CC0003%3A0%2CC0002%3A0%2CC0004%3A0&ep.user_agent_string=Mozilla%2F5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F157.0.0.0%20Safari%2F537.36%20Edg%2F157.0.0.0&ep.gtm_container_id=GTM-MLWBHX9W&ep.gtm_container_version=70&ep.timestamp=2026-11-11T18%3A55%3A46.756-05%3A00&ep.client_id_2=not%20set&ep.content_language=en&ep.previous_page_url=&ep.account_type=personal&ep.page_name=personal&ep.page_hostname="
		"www.tangerine.ca&ep.previous_page_path=&ep.previous_page_hostname=&ep.content_group=visitor-web&ep.adobe_ecid=&_et=31005&tfd=143093", 
		"Method=POST", 
		"Resource=0", 
		"RecContentType=text/plain", 
		"Referer=https://www.tangerine.ca/en/personal", 
		"Snapshot=t31.inf", 
		"Mode=HTML", 
		"EncType=", 
		LAST);

	web_add_auto_header("Sec-Fetch-Site", 
		"cross-site");

	web_add_auto_header("Sec-Fetch-Storage-Access", 
		"none");

	web_custom_request("collect_2", 
		"URL=https://analytics.google.com/g/s/collect?_gsid=Nthi1IV-i32633AXvoRz2J9h5rXyUVnVGg&gtm=45g92e6ba1v878796413za20kzb9174847117zd9174847117xf4", 
		"Method=POST", 
		"Resource=0", 
		"RecContentType=text/plain", 
		"Referer=https://www.tangerine.ca/", 
		"Snapshot=t32.inf", 
		"Mode=HTML", 
		"EncType=", 
		LAST);

	web_add_auto_header("Sec-Fetch-Mode", 
		"cors");

	web_custom_request("set-consent", 
		"URL=https://adobedc.demdex.net/ee/v1/privacy/set-consent?configId=d0c6161f-daf0-401c-b2bf-ba01da52d928&requestId=eb05c0b8-cd9c-4720-ace5-f9a522d2abbc", 
		"Method=POST", 
		"Resource=0", 
		"RecContentType=application/json", 
		"Referer=https://www.tangerine.ca/en/personal", 
		"Snapshot=t33.inf", 
		"Mode=HTML", 
		"EncType=text/plain; charset=UTF-8", 
		"Body={\"consent\":[{\"value\":{\"general\":\"in\"},\"version\":\"1.0\",\"standard\":\"Adobe\"}],\"query\":{\"identity\":{\"fetch\":[\"ECID\",\"CORE\"]}},\"identityMap\":{\"ECID\":[{\"id\":\"86123182909378347043684817210902965393\"}]},\"meta\":{\"state\":{\"domain\":\"tangerine.ca\",\"cookiesEnabled\":true}}}", 
		EXTRARES, 
		"Url=https://www.google.ca/ads/ga-audiences?v=1&t=sr&slf_rd=1&_r=4&ngs=1&ibt=1&tid=G-RFBV4QJDD5&cid=1478828077.1794441375&gtm=45g92e6ba1v878796413za20kzb9174847117zd9174847117xf4&rcb=16&aip=1&dma=0&gcs=G111&gcd=13r3v3r3r7l1&npa=1&frm=0&tag_exp=115938466~115938468~118897920~118897930~120213116~120385422~120412528~120420416~120469145~120469153~121246026~121246034~123329123~124170881&z=1195340933", "Referer=https://www.tangerine.ca/", ENDITEM, 
		LAST);

	web_add_auto_header("Sec-Fetch-Mode", 
		"no-cors");

	lr_think_time(14);

	web_custom_request("collect_3", 
		"URL=https://edge.adobedc.net/ee/or2/v1/collect?configId=d0c6161f-daf0-401c-b2bf-ba01da52d928&requestId=bfdbc606-89c4-4fbd-8e28-94e8157fe5c4", 
		"Method=POST", 
		"Resource=0", 
		"Referer=https://www.tangerine.ca/", 
		"Snapshot=t34.inf", 
		"Mode=HTML", 
		"EncType=text/plain; charset=utf-8", 
		"Body={\"events\":[{\"xdm\":{\"eventType\":\"web.webinteraction.linkClicks\",\"web\":{\"webInteraction\":{\"name\":\"Accept All\",\"region\":\"onetrust-button-group\",\"type\":\"other\",\"URL\":\"https://www.tangerine.ca/en/personal\",\"linkClicks\":{\"value\":1}},\"webPageDetails\":{\"URL\":\"https://www.tangerine.ca/en/personal\"},\"webReferrer\":{\"URL\":\"\"}},\"device\":{\"screenHeight\":1080,\"screenWidth\":1920,\"screenOrientation\":\"landscape\"},\"environment\":{\"type\":\"browser\",\""
		"browserDetails\":{\"viewportWidth\":1897,\"viewportHeight\":964}},\"placeContext\":{\"localTimezoneOffset\":300,\"localTime\":\"2026-11-11T18:56:50.935-05:00\",\"ianaTimezone\":\"America/Toronto\"},\"timestamp\":\"2026-11-11T23:56:50.935Z\",\"implementationDetails\":{\"name\":\"https://ns.adobe.com/experience/alloy/reactor\",\"version\":\"2.34.1+2.37.0\",\"environment\":\"browser\"}},\"data\":{\"__adobe\":{\"analytics\":{\"contextData\":{\"a\":{\"activitymap\":{\"page\":\"Personal Banking Online: "
		"Digital Banking in Canada | Tangerine\",\"link\":\"Accept All\",\"region\":\"onetrust-button-group\",\"pageIDType\":1}}}}}}}],\"query\":{\"identity\":{\"fetch\":[\"ECID\",\"CORE\"]}},\"meta\":{\"queueTimeMillis\":29968,\"state\":{\"domain\":\"tangerine.ca\",\"cookiesEnabled\":true,\"entries\":[{\"key\":\"kndctr_0AAF22CE52827A080A490D4D_AdobeOrg_cluster\",\"value\":\"or2\"},{\"key\":\"kndctr_0AAF22CE52827A080A490D4D_AdobeOrg_identity\",\"value\":\""
		"CiY4NjEyMzE4MjkwOTM3ODM0NzA0MzY4NDgxNzIxMDkwMjk2NTM5M1IQCLCvreicNBgBKgNPUjIwA_ABsK-t6Jw0\"},{\"key\":\"kndctr_0AAF22CE52827A080A490D4D_AdobeOrg_consent\",\"value\":\"general=in\"}]}}}", 
		LAST);

	web_custom_request("collect_4", 
		"URL=https://edge.adobedc.net/ee/or2/v1/collect?configId=d0c6161f-daf0-401c-b2bf-ba01da52d928&requestId=8c97fae5-9277-4f19-abc7-b0c398671d7a", 
		"Method=POST", 
		"Resource=0", 
		"Referer=https://www.tangerine.ca/", 
		"Snapshot=t35.inf", 
		"Mode=HTML", 
		"EncType=text/plain; charset=utf-8", 
		"Body={\"events\":[{\"xdm\":{\"eventType\":\"web.webinteraction.linkClicks\",\"web\":{\"webInteraction\":{\"name\":\"Accept All\",\"region\":\"onetrust-button-group\",\"type\":\"other\",\"URL\":\"https://www.tangerine.ca/en/personal\",\"linkClicks\":{\"value\":1}},\"webPageDetails\":{\"URL\":\"https://www.tangerine.ca/en/personal\"},\"webReferrer\":{\"URL\":\"\"}},\"device\":{\"screenHeight\":1080,\"screenWidth\":1920,\"screenOrientation\":\"landscape\"},\"environment\":{\"type\":\"browser\",\""
		"browserDetails\":{\"viewportWidth\":1897,\"viewportHeight\":964}},\"placeContext\":{\"localTimezoneOffset\":300,\"localTime\":\"2026-11-11T18:57:02.212-05:00\",\"ianaTimezone\":\"America/Toronto\"},\"timestamp\":\"2026-11-11T23:57:02.213Z\",\"implementationDetails\":{\"name\":\"https://ns.adobe.com/experience/alloy/reactor\",\"version\":\"2.34.1+2.37.0\",\"environment\":\"browser\"}},\"data\":{\"__adobe\":{\"analytics\":{\"contextData\":{\"a\":{\"activitymap\":{\"page\":\"Personal Banking Online: "
		"Digital Banking in Canada | Tangerine\",\"link\":\"Accept All\",\"region\":\"onetrust-button-group\",\"pageIDType\":1}}}}}}}],\"query\":{\"identity\":{\"fetch\":[\"ECID\",\"CORE\"]}},\"meta\":{\"queueTimeMillis\":18689,\"state\":{\"domain\":\"tangerine.ca\",\"cookiesEnabled\":true,\"entries\":[{\"key\":\"kndctr_0AAF22CE52827A080A490D4D_AdobeOrg_cluster\",\"value\":\"or2\"},{\"key\":\"kndctr_0AAF22CE52827A080A490D4D_AdobeOrg_identity\",\"value\":\""
		"CiY4NjEyMzE4MjkwOTM3ODM0NzA0MzY4NDgxNzIxMDkwMjk2NTM5M1IQCLCvreicNBgBKgNPUjIwA_ABsK-t6Jw0\"},{\"key\":\"kndctr_0AAF22CE52827A080A490D4D_AdobeOrg_consent\",\"value\":\"general=in\"}]}}}", 
		LAST);

	return 0;
}