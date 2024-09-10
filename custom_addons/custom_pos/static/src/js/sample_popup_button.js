/** @odoo-module */
import { AbstractAwaitablePopup } from "@point_of_sale/app/popup/abstract_awaitable_popup";
import { useRef } from "@odoo/owl";
import { _t } from "@web/core/l10n/translation";

export class SamplePopupButton extends AbstractAwaitablePopup {

    static template = "custom_pos.SamplePopupButton";
    setup() {
       super.setup();
       this.inputRef = useRef("inputRef");
    }
    static defaultProps = {
        closePopup: _t("Cancel"),
        confirmText: _t("Save"),
        title: 'Enter Quantity',
    };
    confirm() {
        const inputValue = this.inputRef.el.value;
        if (inputValue && !isNaN(inputValue)) {
            console.log("========")
            this.props.resolve({ confirmed: true, value: parseInt(inputValue) });
            this.props.close();
        }
        else {
            console.log("Please enter a valid number.");
        }
    }
    
}

