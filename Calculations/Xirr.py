# https://github.com/peliot/XIRR-and-XNPV/blob/master/financial.py
import CalculationAPI
import datetime
from scipy import optimize



class Xirr(CalculationAPI.CalculationAPI):

    def __call__(self, fundID, endDate):
        # query for values
        # endDate = datetime.datetime.strptime('4/2/18', '%m/%d/%y')
#        cashflows = self.CashFlowDB.queryDB(
#            """SELECT cfDate, cashValue
#            FROM CashFlowJoinType
#            WHERE fundID = '{}' AND cfDate <= '{}' AND (result = '{}' OR result = '{}')""".format(
#                fundID, endDate, 'Contribution', 'Distribution')).fetchall()
        cashflows = self.CashFlowDB.queryDB(" SELECT cfDate, cashValue FROM `CommitmentJoinDistribution` "
                                            "WHERE fundID = '{0}' AND cfDate <= '{1}' UNION "
                                            "(SELECT (SELECT cfDate FROM CashFlow "
                                            "WHERE fundID = '{0}' AND cfDate <= '{1}' "
                                            "ORDER BY cfDate DESC LIMIT 1) as cfDate, "
                                            "totalNav('{0}','{1}') as cashValue) order by cfDate ASC;".format(fundID, endDate)).fetchall()

        print "*** FUND: " + fundID + " ****"
        print cashflows
        print "************"

        return self._xirr(cashflows)

    def _xnpv(self, rate, cashflows):
        """
        Calculate the net present value of a series of cashflows at irregular intervals.
        Arguments
        ---------
        * rate: the discount rate to be applied to the cash flows
        * cashflows: a list object in which each element is a tuple of the form (date, amount), where date is a python datetime.date object and amount is an integer or floating point number. Cash outflows (investments) are represented with negative amounts, and cash inflows (returns) are positive amounts.

        Returns
        -------
        * returns a single value which is the NPV of the given cash flows.
        Notes
        ---------------
        * The Net Present Value is the sum of each of cash flows discounted back to the date of the first cash flow. The discounted value of a given cash flow is A/(1+r)**(t-t0), where A is the amount, r is the discout rate, and (t-t0) is the time in years from the date of the first cash flow in the series (t0) to the date of the cash flow being added to the sum (t).
        * This function is equivalent to the Microsoft Excel function of the same name.
        """

        chron_order = sorted(cashflows, key=lambda x: x[0])
        t0 = chron_order[0][0]  # t0 is the date of the first cash flow

        return sum([cf / (1 + rate) ** ((t - t0).days / 365.0) for (t, cf) in chron_order])

    def _xirr(self, cashflows, guess=0.1):
        """
        Calculate the Internal Rate of Return of a series of cashflows at irregular intervals.
        Arguments
        ---------
        * cashflows: a list object in which each element is a tuple of the form (date, amount), where date is a python datetime.date object and amount is an integer or floating point number. Cash outflows (investments) are represented with negative amounts, and cash inflows (returns) are positive amounts.
        * guess (optional, default = 0.1): a guess at the solution to be used as a starting point for the numerical solution.
        Returns
        --------
        * Returns the IRR as a single value

        Notes
        ----------------
        * The Internal Rate of Return (IRR) is the discount rate at which the Net Present Value (NPV) of a series of cash flows is equal to zero. The NPV of the series of cash flows is determined using the xnpv function in this module. The discount rate at which NPV equals zero is found using the secant method of numerical solution.
        * This function is equivalent to the Microsoft Excel function of the same name.
        * For users that do not have the scipy module installed, there is an alternate version (commented out) that uses the secant_method function defined in the module rather than the scipy.optimize module's numerical solver. Both use the same method of calculation so there should be no difference in performance, but the secant_method function does not fail gracefully in cases where there is no solution, so the scipy.optimize.newton version is preferred.
        """

        try:
            result = optimize.newton(lambda r: self._xnpv(r, cashflows), guess)
        except Exception as e:
            print e
            result = "ERROR"
        return self.giveResult(result)


a = Xirr()
a('CCDD062016AF', '18/4/2')