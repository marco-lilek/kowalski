function toggleDisplay(tab) {
  console.log(tab);
  // Show only if its a discogs URL
  if (tab.url.match(/www.discogs.com/)) {
    chrome.pageAction.show(tab.id);
  } else {
    chrome.pageAction.hide(tab.id);
  } 
}

// Works when the client reloads the tab
chrome.tabs.onUpdated.addListener(function(tabId, changeInfo, tab) {
  console.log(changeInfo);
  if (changeInfo.status === 'complete') {
    toggleDisplay(tab);
  }
});

// Works when the client switches to the tab
chrome.tabs.onActivated.addListener(function(activeInfo) {
  chrome.tabs.query({active: true}, function(activeTabs) {
    for (i = 0; i < activeTabs.length; i++) {
      toggleDisplay(activeTabs[i]);
    }
  });
});

