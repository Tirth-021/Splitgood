let countElement = 0;
		document.querySelector('#submitbtn').addEventListener('click',function(e){
			e.preventDefault();
			let name = document.querySelector('.name').value;
			let expenseDate = document.querySelector('.expenseDate').value;
			let amount = document.querySelector('.amount').value;
			let table = document.querySelector('.expense-data tbody');
			let tabletr = table.getElementsByTagName('tr');

			let date = new Date(expenseDate);
			let year = date.getFullYear();
			let month = date.getMonth()+1;
			let inputDate = String(date.getDate()).padStart(2,'0');
			let outputDate = inputDate+'-'+month+'-'+year;
			if(name == ""){
				alert('Enter Name');
				return false;
			}else if(expenseDate == ""){
				alert('Enter Date');
				return false;
			}else if(amount == ""){
				alert('Enter Amount');
				return false;
			}
			if(name && date && amount){
				table.innerHTML += '<tr><td><input id="label-'+countElement+'" type="checkbox"><label for="label-'+countElement+'"></label></td><td>'+name+'</td><td>$'+amount+'</td><td>'+ outputDate+'</td><td><button class="remove" onclick="this.parentNode.parentNode.remove();">X</button></td></tr>';
				document.querySelector('.name').value = "";
				document.querySelector('.expenseDate').value = "";
				document.querySelector('.amount').value ="";
				countElement++;
			}
		});
		document.querySelector('.selectElement input').addEventListener('click',function(e){
			let labelCheckbox = document.querySelectorAll('.expense-data input[type="checkbox"]');
			let deleteButton = document.querySelector('.deleteBtn');
			for(let i = 0; i < labelCheckbox.length; i++ ){
				if(this.checked == true ){
					labelCheckbox[i].checked = true;
				}else{
					labelCheckbox[i].checked = false;
					deleteButton.addEventListener('click',function(e){
						e.preventDefault();
						labelCheckbox[i].parentNode.parentNode.remove();
						document.querySelector('.selectElement input').checked = false;
					});

				}
			}
		});
		document.querySelector('.searchName').addEventListener('keyup',function(e){
			let filter = document.querySelector('.searchName').value.toUpperCase();
			let expTable = document.querySelector('.expense-data');
			let expTr = expTable.getElementsByTagName('tr');
			for(let i = 0; i < expTr.length; i++){
				let expName = expTr[i].getElementsByTagName('td')[1];
				if(expName){
					let txtVal = expName.textContent || expName.innerHTML;
					if(txtVal.toUpperCase().indexOf(filter) > -1){
						expTr[i].style.display = '';

					}else{
						expTr[i].style.display = 'none';
					}
				}
			}
		});