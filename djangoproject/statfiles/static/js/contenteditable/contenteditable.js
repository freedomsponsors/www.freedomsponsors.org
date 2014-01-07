angular.module('contenteditable', []).
	directive('contenteditable', function () {
	return {
		restrict: 'A', // only activate on element attribute
		require: '?ngModel', // get a hold of NgModelController
		link: function (scope, element, attrs, ngModel) {
			if (!ngModel) return; // do nothing if no ng-model

			// Specify how UI should be updated
			ngModel.$render = function () {
				element.html(ngModel.$viewValue || '');
			};

			// Listen for change events to enable binding
			element.on('blur keyup change', function () {
				scope.$apply(readViewText);
			});

			// No need to initialize, AngularJS will initialize the text based on ng-model attribute

			// Write data to the model
			function readViewText() {
				var html = element[0].innerHTML;
				// When we clear the content editable the browser leaves a <br> behind
				// If strip-br attribute is provided then we strip this out
				if (attrs.stripBr) {
					html = html.replace(/<br>/g,"");
					element[0].innerHTML = html; // Firefox replaces caret at beginning after this
					placeCaretAtEnd(element[0]); // So we fix it here, otherwise if you type "html" you will get "lmth"
				}
				ngModel.$setViewValue(html);
			}
			
			// Places de caret at de end of element
			function placeCaretAtEnd(element) {
				element.focus();
				if (typeof window.getSelection != "undefined"
						&& typeof document.createRange != "undefined") {
					var range = document.createRange();
					range.selectNodeContents(element);
					range.collapse(false);
					var sel = window.getSelection();
					sel.removeAllRanges();
					sel.addRange(range);
				} else if (typeof document.body.createTextRange != "undefined") {
					var textRange = document.body.createTextRange();
					textRange.moveToElementText(element);
					textRange.collapse(false);
					textRange.select();
				}
			}
		}
	};
});