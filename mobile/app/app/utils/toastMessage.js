import { ToastDuration, Toasty } from '@triniwiz/nativescript-toasty';


export default {
    info(text) {
        const toast = new Toasty({ text: text});
        toast.setToastDuration(ToastDuration.SHORT)
        toast.textColor = 'black'
        toast.backgroundColor = 'green';                 
        toast.show();
    },
    warning(text) {
        const toast = new Toasty({ text: text});
        toast.setToastDuration(ToastDuration.LONG)
        toast.textColor = 'black'
        toast.backgroundColor = 'yellow'; 
        toast.show();

    },
    error(text) {
        const toast = new Toasty({ text: text});
        toast.setToastDuration(ToastDuration.LONG)
        toast.textColor = 'black'        
        toast.backgroundColor = 'red'; 
        toast.show();

    },


};
