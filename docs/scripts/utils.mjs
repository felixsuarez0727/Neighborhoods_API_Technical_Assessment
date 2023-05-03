export function hasToRefetchAddresses () {
    const date = new Date(localStorage.getItem("addresses_date")?.substring(1,11))
   
    return( isDistinctDay(date) )
}

export function isDistinctDay(date){
    const now = new Date(JSON.stringify(new Date()).substring(1,11));
    return !(now.getDate() === date.getDate() &&  now.getFullYear() === date.getFullYear() &&  now.getMonth() === date.getMonth());
}
