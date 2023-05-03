export function removeStorage () {
    localStorage.removeItem("addresses")
    localStorage.removeItem("addresses_date")
}

export function setStorage (addresses) {
    localStorage.setItem("addresses", JSON.stringify(addresses));
    localStorage.setItem("addresses_date", JSON.stringify(new Date()))
}

export function getStoredAddresses(){
    return JSON.parse(localStorage.getItem("addresses")) || []
} 
