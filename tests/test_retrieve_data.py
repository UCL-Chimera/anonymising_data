from retrieve_data.retrieve_data import RetrieveData


def test_get_query(retrieval):
    sql = retrieval.get_query(testing=True)
    assert(sql == "SELECT pd.DurableKey, pd.BirthDate, fvf.NumericValue, fvf.TakenInstant\n"
                  "FROM FlowsheetValueFact AS fvf\n"
                  "JOIN FlowsheetRowDim AS frd\n"
                  "ON fvf.FlowsheetRowKey = frd.FlowsheetRowKey\n"
                  "JOIN PatientDim AS pd\n"
                  "ON pd.DurableKey = fvf.PatientDurableKey\n"
                  "WHERE frd.FlowsheetRowEpicId = 6")


def test_get_data(retrieval):
    data = retrieval.get_data(testing=True)
    assert(data is not None)
    assert(len(data) == 3)
    data1 = data[0]
    assert(len(data1) == 4)
    assert(data1[0] == 91)
    assert(data1[1] == '1999-02-07')
    assert(data1[2] == 37.1)
    assert(data1[3] == '2022-05-03 08:30:02')
