function $$(element) {
  if (arguments.length > 1) {
    for (var i = 0, elements = [], length = arguments.length; i < length; i++)
      elements.push($$(arguments[i]));
    return elements;
  }
  if (typeof element == "string")
    element = document.getElementById(element);
  return element;
}

	function doSearch(stext, sPageName,bTitle)
		{
		if(null==bTitle) bTitle=false;
		if (sPageName == "" || sPageName == null)
			{
			var sSearchPage="search.htm";
			}
		else
			{
			var sSearchPage="_search_"+sPageName+".htm";
			}
		if ($$("fra_contents") != null)
			{
			window.open(sSearchPage+"?search="+stext+(bTitle?"&searchTitle=true":""), "fra_contents");
			$$("fra_contents").style.display="";
			}
		else if ($$("basefrm") != null)
			{
			window.open(sSearchPage+"?search="+stext+(bTitle?"&searchTitle=true":""), "basefrm");
			}
		else
			{
			location.href = sSearchPage+"?search="+stext+"&type=noframes"+(bTitle?"&searchTitle=true":"");

        }
   	        if($$('imgtabs')!=null)
   	            $$('imgtabs').src='images/skins/tabs_tabs_search.gif';
            if($$('tdSearchRes')!=null)
                tabtoggle($$('tdSearchRes'));  			
	}
	function doMark() {	 
	    var sSearchPage = "_bookmark.htm";	   
	    if ($$("fra_contents") != null) {
	        window.open(sSearchPage, "fra_contents");
	        $$("fra_contents").style.display = "";
	    }
	    else if ($$("basefrm") != null) {
	        window.open(sSearchPage, "basefrm");
	    }
	    else {
	        location.href = sSearchPage;
	    }
	    if ($$('tdBookMark') != null)
	        tabtoggle($$('tdBookMark'));
	}
	function displayIndex()
	{
		if ($$("fra_contents") != null)
			{
			window.open("_keywordindex.htm", "fra_contents");
			}
		else if ($$("basefrm") != null)
			{
			window.open("_keywordindex.htm", "basefrm");
			}
		else if ($$("div_javascript_contents") != null)
			{
			$$("div_javascript_index").style.display="";
			$$("div_javascript_contents").style.display="none";
			}
	    else
	        {
			location.href = "_index.htm";
	        }
        if($$('imgtabs')!=null)
            $$('imgtabs').src='images/skins/tabs_tabs_index.gif';
        if($$('tdIndex')!=null)
         tabtoggle($$('tdIndex'));
	}


	function displayContents()
		{
		if ($$("fra_contents") != null)
			{
			window.open("contentTree.htm", "fra_contents");
			}
		else if ($$("basefrm") != null)
			{
			window.open("contentTree.htm", "basefrm");
			}
		else if ($$("div_javascript_contents") != null)
			{
			$$("div_javascript_index").style.display="none";
			$$("div_javascript_contents").style.display="";
			}
	    else
	        {
			location.href = "contentTree.htm";
	        }
        if($$('imgtabs')!=null)
            $$('imgtabs').src='images/skins/tabs_tabs_contents.gif';
        if($$('tdContentTree')!=null)
            tabtoggle($$('tdContentTree')); 	        
	}

	function addtofav()
		{
		//if (document.all)
			{
			//if there is a basefrm frame then get the URL from there, otherwise get the url for this page.
			if ($$("basefrm") == null)
				{
				 
				var sPageName = sFavURL.substr(sFavURL.lastIndexOf("/")+1);
				}
			else
				{
				//FRAMES - get URL from the frame
			 
				var sPageName = window.basefrm.document.title;// sPageURL.substr(sPageURL.lastIndexOf("/") + 1);
				 
				}

			//Remove any parameters from the url (eg. page.aspx?search=X)
          
			//Remove any parameters from the pagename (eg. page.aspx?search=X)
			if (sPageName.indexOf("?") != -1)
			{
			    sPageName=sPageName.substr(0,sPageName.lastIndexOf("?"));
			}

			//remove any %20 codes (space codes)
            sPageName = sPageName.replace(/%20/g, " ");
            sFavURL = getCurPageUrl();
			var sTitle=sPageName;
			 
			if ($$("basefrm") == null)
                {
                // --FLAT--
    			window.external.AddFavorite(sFavURL,sTitle);
                }
            else
                {
                // --FRAMES--
                    window.external.AddFavorite(sFavURL, sTitle); //+ "?" + sPageName
                }
                

			}
		}
	


	function printPage()
		{
		//if the basefrm frame exists then print the contents
		if ($$("basefrm") != null)
			{
			printframe();
			}
		else
			{
			//If this is IE then print the cell containing the page HTML. If this is another browser then print the entire page.
			if (navigator.userAgent.toLowerCase().indexOf("ie") == -1)
				{
				//Current browser is not IE
				window.print();
				}
			else
				{
				//Current browser is IE
				print_noframes();
				}
			}
		}


	function printframe()
		{
		//print the basefrm frame
		window.frames['basefrm'].focus(); 
		window.frames['basefrm'].print();
		}


	function print_noframes()
		{
		var printIframe = document.createElement("IFRAME");
		document.body.appendChild(printIframe);
		var printDocument = printIframe.contentWindow.document;
		printDocument.designMode = "on";
		printDocument.open();
		var currentLocation = document.location.href;
		currentLocation = currentLocation.substring(0, currentLocation.lastIndexOf("/") + 1);
		var htmlcontent = $$("td_noframes_main");
		printDocument.write("<html><head></head><body>" + htmlcontent.innerHTML + "</body></html>");
		printDocument.close();

		try
			{
			if (document.all)
				{
				var oLink = printDocument.createElement("link");
				oLink.setAttribute("href", currentLocation + "pgstyles.css", 0);
				oLink.setAttribute("type", "text/css");
				oLink.setAttribute("rel", "stylesheet", 0);
				printDocument.getElementsByTagName("head")[0].appendChild(oLink);
				printDocument.execCommand("Print");
				}
			else
				{
				printDocument.body.innerHTML = "<link rel='stylesheet' type='text/css' href='" + currentLocation + "pgstyles.css'></link>" + printDocument.body.innerHTML;
				printIframe.contentWindow.print();
				}
			}
		catch(ex)
			{
			}
		document.body.removeChild(printIframe);
		}

		function getCurPageUrl() {
		    if ($$("basefrm") == null) {
		        //FLAT - get URL from this page
		        var sPageURL = String(location.href);
		        var sPageName = sPageURL.substr(sPageURL.lastIndexOf("/") + 1);
		    }
		    else {
		        var sPageURL = String(window.basefrm.location.href);
		        if (sPageURL.toLowerCase().indexOf("?") != -1) {
		            sPageName = sPageURL.substr(sPageURL.lastIndexOf("?") + 1, sPageURL.length - sPageURL.lastIndexOf("?"));
		            if ("undefined" == typeof (sPageName)) sPageName = "";
		            sPageURL = sPageURL.substr(0, sPageURL.lastIndexOf("?"));
		        }
		        sPageURL = sPageURL.substr(0, sPageURL.lastIndexOf("/"));

		        var sPageURL = sPageURL + "/default.htm?" + sPageName;
		    }
		    return sPageURL;
        }
	function showPageHref()
	{

	    sPageURL = getCurPageUrl();
	    //Set the table cell innerHTML
	    var sHTML = ""		;
	    sHTML = sHTML + "<table style='width:400px;height:165px;background-image:url(images/pageurl_back.gif);cellpadding:24px'><tr style='height:35px'><td align=right><img src='images/close_mover.gif' style='cursor:pointer;' onclick='closepagelinkform()'><tr><td valigh='top'>&nbsp;<textarea style='width:98%'  rows=4>"+sPageURL+"</textarea></td></tr><tr ><td align=right valign=top ><input type=button class='btnstyle' onclick=\"clip('"+sPageURL+"')\" value='Copy'>&nbsp;</td></tr></table>";

	    $$("tdpageurl").innerHTML=sHTML;
	    $$("tblpageurl").style.display="";
	}

    function closepagelinkform()
        {
        $$("tblpageurl").style.display="none";
        }

	function loadPage()
		{
		    setTimeout(function () {
		        var pageIds = findParamByUrl("pageIds");
		        if ('' != pageIds) {
		            pageIds = pageIds.replace(/%20/g, " ");
		            HighlightPage(pageIds, true);
		            return;
		        }
		        var pageId = findParamByUrl("pageId");
		        if ('' != pageId) {
		            pageId = pageId.replace(/%20/g, " ");
		            HighlightPage(pageId,false);
		            return;
		        }		     
		        var title = findParamByUrl("title");
		        if ("" != title) {
		            title = title.replace(/%20/g, " ");
		            doSearch(title, "", true);
		            return;
		        }
		        var keys = findParamByUrl("search");
		        if ("" != keys) {
		            keys = keys.replace(/%20/g, " ");
		            doSearch(keys);
		            return;
		        }
		    }, 500);
		}


			
		function previouspage()
			{
				onclick = history.back()
			}
			
		function nextpage()
			{
				onclick = history.forward()
			}

		function showhomepage(homepage)
			{
			if ($$("basefrm") != null)
				{
				window.open(homepage, "basefrm");
				}
			else
				{
				location.href = homepage;
				}
			}
			
		function browse()
			{
			if ($$("basefrm") != null)
				{
				window.open("contentTree.htm", "basefrm");
				}
			else
				{
				location.href = "contentTree.htm";
				}
			}

		function showaskpage()
			{
			if ($$("basefrm") != null)
				{
				window.open("ask.htm", "basefrm");
				}
			else
				{
				location.href = "ask.htm";
				}
			}


		function showOptions()
			{			
			if ($$("tbloptions").style.display=="")
				{
				$$("tbloptions").style.display="none";
				}
			else
				{
				$$("tbloptions").style.display="";
				$$("tbloptions").focus();
				//position the options list below the options button
				$$("tbloptions").style.top=$$("imgoptions").offsetTop+$$("imgoptions").offsetHeight;
				$$("tbloptions").style.left=$$("imgoptions").offsetLeft+$$("imgoptions").offsetWidth-198;
				}
			}
function clip(tocopy)
{
    window.clipboardData.setData("Text",tocopy); 
}
function findParamByUrl(parmaName)
{					    	
	var atoms=window.location.href.split("?");
	if(atoms.length!=2) return "";
	atoms=atoms[1].split("&");
	for(var shift=0;shift< atoms.length;shift++)
	{
		if(atoms[shift].toLowerCase().indexOf(parmaName.toLowerCase())>-1)
		{
			var atoms1=atoms[shift].split('=');
			if(atoms1.length==2)
				return atoms1[1];
		}
	}
	return "";
}
function searchKeyPress(searchtext,e)
	{
	
	var key;
    if(window.event)		
        key = window.event.keyCode;     //IE		
    else		
        key = e.which;     //fs
	
	if(key == 13)
		{    
		    doSearch(searchtext);
		    return false;
		}
	else
		{
		return true;
		}
}
function toggleNavBar() {
    if ($$('spNavBar').className == 'NP4') {
        $$('spNavBar').className = 'NP3';
        $$("tdMainContent").style.display = "none";
    }
    else {
        $$('spNavBar').className = 'NP4';
        $$("tdMainContent").style.display = "";
    }
}
function getParentNodeByTagName(idd, findTag) {
    var node = $$(idd);
    var shift = 0;
    while (node.tagName != findTag && shift++ < 20) {
        node = node.parentNode;
    }
    if (node.tagName == findTag)
        return node;
    else
        return null;
}