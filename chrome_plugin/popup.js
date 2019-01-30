function sendMessage(args) {
	chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
		var tab = tabs[0];

		console.log(args)
		var xhr = new XMLHttpRequest();
		xhr.onreadystatechange = function() {
			if (xhr.readyState == 4) {
				chrome.pageAction.setIcon({tabId: tab.id, path: 'accept.png'}, function() {
			  window.close()

				});
			}
		}
		xhr.open("GET", 'http://localhost:5000/?' 
			+ 'url=' + tab.url 
			+ '&type=' + args.type, true);
		xhr.send();
	})
}

document.addEventListener('DOMContentLoaded', function() {
	var inputs = document.querySelectorAll('input');
	for (var i = 0; i < inputs.length; i++) {
		inputs[i].addEventListener('click', function(e) { 
						console.log(e.target.id)
						sendMessage({type: e.target.id})
		})
	}
})
