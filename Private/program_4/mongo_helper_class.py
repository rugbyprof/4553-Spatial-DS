from pymongo import MongoClient
import pprint as pp


class mongoHelper(object):
    def __init__(self):
        self.client = MongoClient()

        self.db_airports = self.client.geo.airports
        self.db_states = self.client.geo.states


    def get_airports_in_poly(self,poly):
        """
        Get airports within some polygon
        Params:
            poly (object): geojson poly
        """
        state_airports = self.db_airports.find( { 'loc' : { '$geoWithin' : { '$geometry' : poly } } })

        ap_list = []
        for ap in state_airports:
            ap_list.append(ap)

        return ap_list

    def get_state_poly(self,state):
        state_poly = self.db_states.find_one({'code' : state})
        return(state_poly['loc'])

    def get_afb_airports(self):

        
        res = self.db_airports.find({"type" : "Military"})

        res_list = []
        for r in res:
            res_list.append(r)

        return res_list

    def get_doc_by_keyword(self,db_name,field,key):
        if db_name == 'airports':
            res = self.db_airports.find({field : {'$regex' : ".*"+key+".*"}})
        else:
            res = self.states.find({field : {'$regex' : ".*"+key+".*"}})
        
        res_list = []
        for r in res:
            res_list.append(r)

        return res_list


    def get_state_by_point(self,point):
        return self.db_states.find_one({'loc':{'$geoIntersects':{'$geometry':{ "type" : "Point","coordinates" : point }}}})

    def get_state_by_name(self,name):
        pass


def main():
    mh = mongoHelper()
    poly = mh.get_state_poly("CA")
    ap = mh.get_airports_in_poly(poly)
    afb = mh.get_afb_airports()
    print(len(afb))
    bykey = mh.get_doc_by_keyword('airports','name','County')

    pp.pprint(bykey)


    # state = mh.get_state_by_point([-95.912512, 41.118327])
    # pp.pprint(state)

if __name__=='__main__':
    main()
