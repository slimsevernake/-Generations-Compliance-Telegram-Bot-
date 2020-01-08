import datetime as dt

from main.entity.document import Document


def is_month(month):
    try:
        dt.datetime.strptime(month, '%B').month
        return True
    except Exception as e:
        print(e)
        return False


def is_year(year):
    return type(year) == int


def is_block_out_dates(block_out_dates):
    if type(block_out_dates) == dict:
        for date in block_out_dates.keys():
            if not date.isdigit():
                return False
        return True
    else:
        return False


def is_unconfirmed(unconfirmed):
    if type(unconfirmed) != list:
        return False
    else:
        for name in unconfirmed:
            if type(name) != str:
                return False
        return True


class BlockOutDates(Document):
    def __init__(self, block_out_dates_details=None, month="January", year=2019, block_out_dates=None, unconfirmed=None):
        super().__init__(
            all_fields=[
                "Month", "Year", "Block Out Dates", "Unconfirmed"
            ],
            all_fields_data_type={
                "Month": str,
                "Year": int,
                "Block Out Dates": dict,
                "Unconfirmed": list
            },
            all_fields_data_format={
                "Month": is_month,
                "Year": is_year,
                "Block Out Dates": is_block_out_dates,
                "Unconfirmed": is_unconfirmed
            },
            non_editable_fields=[],
            document_details=block_out_dates_details
        )
        if unconfirmed is None:
            unconfirmed = []
        if block_out_dates is None:
            block_out_dates = {}
        if block_out_dates_details is None:
            self.set_datafield("Year", year)
            self.set_datafield("Month", month)
            self.set_datafield("Block Out Dates", block_out_dates)
            self.set_datafield("Unconfirmed", unconfirmed)

    def get_block_out_dates_str(self):
        msg = "*** No Records ***"
        is_empty_details = True
        for field in self.all_fields:
            is_empty_details &= self.get_datafield(field) is None
        if not is_empty_details:
            msg = "Block Out Dates for {} {}\n\n".format(self.get_datafield("Month"), self.get_datafield("Year"))
            for date in sorted(self.get_datafield("Block Out Dates").keys(), key=lambda x: int(x)):
                msg += "{}: ".format(date)
                if len(self.get_datafield("Block Out Dates")[date]) > 0:
                    msg += "{}".format(self.get_datafield("Block Out Dates")[date][0])
                    for name_pos in range(1, len(self.get_datafield("Block Out Dates")[date])):
                        msg += ", {}".format(self.get_datafield("Block Out Dates")[date][name_pos])
                msg += "\n"
            msg += "\n" + "Unconfirmed Members: \n"
            if len(self.get_datafield("Unconfirmed")) > 0:
                msg += "{}".format(self.get_datafield("Unconfirmed")[0])
                for name_pos in range(1, len(self.get_datafield("Unconfirmed"))):
                    msg += ", {}".format(self.get_datafield("Unconfirmed")[name_pos])
        msg += "\n"
        return msg

    def get_member_block_out_dates_list(self, member_name):
        res = []
        for date in sorted(self.get_datafield("Block Out Dates").keys(), key=lambda x: int(x)):
            if member_name in self.get_datafield("Block Out Dates")[date]:
                res.append(date)
        return res

    def get_member_block_out_dates_str(self, member_name):
        member_block_out_dates_list = self.get_member_block_out_dates_list(member_name)
        msg = "Block Out Dates for {} in {} {}\n\n".format(member_name, self.get_datafield("Month"), self.get_datafield("Year"))
        msg += "Dates Blocked: "
        if len(member_block_out_dates_list) > 0:
            msg += "{}".format(member_block_out_dates_list[0])
            for date_pos in range(1, len(member_block_out_dates_list)):
                msg += ", {}".format(member_block_out_dates_list[date_pos])
        msg += "\nDates Available: "
        available_dates = sorted(
            list(
                set(
                    self.get_datafield("Block Out Dates").keys()) - set(member_block_out_dates_list)
            ),
            key=lambda x: int(x)
        )
        if len(available_dates) > 0:
            msg += "{}".format(available_dates[0])
            for date_pos in range(1, len(available_dates)):
                msg += ", {}".format(available_dates[date_pos])
        msg += "\n"
        return msg

    def get_dates_str(self):
        dates = sorted(list(self.get_datafield("Block Out Dates").keys()), key=lambda x: int(x))
        msg = "All Serving Dates for {} {}: ".format(self.get_datafield("Month"), self.get_datafield("Year"))
        if len(dates) > 0:
            msg += "{}".format(dates[0])
            for i in range(1, len(dates)):
                msg += ", {}".format(dates[i])
        msg += "\n"
        return msg

    def update_unconfirmed(self, member_name):
        new_unconfirmed = self.get_datafield("Unconfirmed")
        if member_name in new_unconfirmed:
            new_unconfirmed.remove(member_name)
        self.update_datafield(
            field="Unconfirmed",
            data=new_unconfirmed
        )

    def update_member_block_out_dates(self, member_name, member_block_out_dates):
        for d in sorted(self.get_datafield("Block Out Dates").keys(), key=lambda x: int(x)):
            if member_name not in self.get_datafield("Block Out Dates")[d] and d in member_block_out_dates:
                self.get_datafield("Block Out Dates")[d].append(member_name)
            elif member_name in self.get_datafield("Block Out Dates")[d] and d not in member_block_out_dates:
                self.get_datafield("Block Out Dates")[d].remove(member_name)