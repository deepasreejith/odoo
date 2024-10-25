/** @odoo-module **/
import { Chatter } from "@mail/core/web/chatter";
import { patch } from "@web/core/utils/patch";

patch(Chatter.prototype, {
    async openAttachmentsView() {
        try {
            console.log('Opening attachments view...');
            // Call doAction to open the kanban view
            const action = {
                type: 'ir.actions.act_window',
                name: 'action_sales_order_attachment',
                res_model: 'ir.attachment',
                view_mode: 'kanban',
                views: [[false, 'kanban']],
                domain: [['res_id', '=', this.props.threadId],
                         ['res_model', '=', this.props.threadModel],],
                context: {
                           active_id: this.props.threadId,
                            active_model: this.props.threadModel,
                            },
            };
            await this.env.services.action.doAction(action);
            console.log('Attachments view opened successfully');
        } catch (error) {
            console.error('Error in action:', error);
        }
    }
});
