from .basedatamodel import BaseDataModel
from .db_schemes import Project
from .enums.DataBaseEnum import DataBaseEnum
from sqlalchemy.future import select
from sqlalchemy import func

class ProjectModel(BaseDataModel):

     def __init__(self, db_client): 
        super().__init__(db_client = db_client)

     #    self.collection = self.db_client[DataBaseEnum.COLLECTION_PROJECT_NAME.value]
        self.db_client = db_client

     @classmethod
     async def create_instance(cls, db_client: object):
        instance = cls(db_client)
     #    await instance.init_collection()
        return instance


     # async def init_collection(self):
     #      all_collections = self.db_client.list_collection_names()
     #      if DataBaseEnum.COLLECTION_PROJECT_NAME.value not in all_collections:
     #           self.collection = self.db_client[DataBaseEnum.COLLECTION_PROJECT_NAME.value]
     #           indexes = Project.get_indexes()
     #           for index in indexes: 
     #                await self.collection.create_index(
     #                     index["key"],
     #                     name = index["name"],
     #                     unique = index["unique"]
     #                )
                       

        
     async def create_project(self, project:Project):

          # result = await self.collection.insert_one(project.dict(by_alias=True, esclude_unset=True))
          # project.project_id = result.inserted_id
          async with self.db_client() as session:
               async with session.begin():
                         session.add(project)
               await session.commit()
               await session.refresh(project)     
          return project

     async def get_project_or_create_one(self, project_id:str):

               # record = await self.collection.find_one({"project_id" == project_id})
               # if record is None:
               #      project = Project(project_id = project_id)
               #      project = await self.create_project(project=project)
               #      return project

               # return project(**record)
               async with self.db_client() as session:
                    async with session.begin():
                         query = select(Project).where(Project.project_id == project_id)
                         result = await session.execute(query)
                         project = result.scalar_one_or_none()
                         if project is None:
                              project = Project(project_id = project_id)
                              project = await self.create_project(project=project)
                              return project
                         return project

     async def get_all_project(self, page:int = 1, page_size:int = 10):

          async with self.db_client() as session:
               async with session.begin():
                    result = await session.execute(select(func.count(Project.project_id)))
                    total_documents = result.scalar_one()
                    total_pages = total_documents // page_size + (1 if total_documents % page_size > 0 else 0)
                    query = select(Project).offset((page - 1) * page_size).limit(page_size)
                    projects = await session.execute(query)
                    return projects.scalars().all(), total_pages
          
          # total_documents = self.collection.count_documents({})

          # total_pages = total_documents // page_size
          # if total_documents % page_size > 0:
          #      total_pages += 1
          
          # cursor = self.collection.find().skip((page -1)*page_size).limit(page_size)
          # projects = []
          # for doc in cursor:
          #      projects.append(Project(**doc))
          # return projects, total_pages 




                




