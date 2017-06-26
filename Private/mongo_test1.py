from pymongo import MongoClient

class MongoHelper(object):
    def __init__(self):
        self.db_airports = MongoClient().geo.airports 
        self.db_states = MongoClient().geo.states

    def get_all_airports(self,type="International"):
        all_airports = self.db_airports.find({"type":type})

        results = []
        for ap in all_airports:
            results.append(ap)

        return results

    def get_doc_by_keyword(self,field,key):
        result = self.db_airports.find({field:{'$regex':'.*'+key+'.*'}})

        res_list = []
        for r in result:
            res_list.append(r)

        return res_list

    def get_airports_in_poly(self,poly):
        state_airports = self.db_airports.find({'loc':{'$geoWithin':{'$geometry':poly}}})
        res_list = []
        for ap in state_airports:
            res_list.append(ap)

        return res_list

    def get_state_by_point(self,point):
        return self.db_states.find_one({"loc":{'$geoIntersects':{'$geometry':point}}})


    def get_state_poly(self,code):
        state = self.db_states.find_one({"code":code})
        return state['loc']

def main():
    mh = MongoHelper()
    gaa = mh.get_all_airports("International")
    #print(gaa)

    county_stuff = mh.get_doc_by_keyword("name","County")
    #print(county_stuff)

    tx_poly = mh.get_state_poly("TX")
    aps = mh.get_airports_in_poly(tx_poly)
    for a in aps:
        print(a)

    print(mh.get_state_by_point([-75.432129,38.825266]))

if __name__=='__main__':
    main()



