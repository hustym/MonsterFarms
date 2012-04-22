# coding: utf-8
#!/usr/bin/python

import os
import math
import bisect

import Proxy
import Entity
import Protocol

from common import ResMgr

class Chunk(object):

    def __init__(self, x, y):
        self.position = x, y
        self.entities = {}

    def addEntity(self, entity):
        self.entities[entity.id] = entity
        self.broadcast(entity, Protocol.enterWorld)

    def removeEntity(self, entity):
        del self.entities[entity.id]
        self.broadcast(entity, Protocol.leaveWorld)

    def broadcast(self, entity, msg):
        for entity in self.entities:
            if isinstance( entity, Proxy):
                entity.talk(msg)


class NoneChunk(Chunk):
    pass


class Space(object):

    CHUNK_HEIGHT = 48
    CHUNK_WIDTH  = 32

    SPACE_DIR = 'spaces/'

    def __init__(self, space_name):
        self.space_path = os.path.join(Space.SPACE_DIR, space_name)
        parser = ResMgr.XMLParser(self.space_path, 'settings.xml')
        xml = parser.parse()
        size = xml.firstChild
        for child in size.childNodes:
            if child.nodeType == child.TEXT_NODE:
                if child.nodeName == 'width':
                    self.width = int(child.data)
                elif child.nodeName == 'height':
                    self.height = int(child.data)

        self.chunk_width = math.ceil(float(self.width) / Space.CHUNK_WIDTH)
        self.chunk_height = math.ceil(float(self.width) / Space.CHUNK_HEIGHT)

        self.chunks={}
        for x in xrange(self.chunk_width):
            for y in xrange(self.chunk_height):
                self.chunks[(x, y)] == Chunk(x, y)

        self.entities = {}
        parser = ResMgr.XMLParser(self.space_path, 'entities.xml')
        xml = parser.parse()
        root = xml.firstChild
        for child in root.childNodes:
            if child.nodeType == child.TEXT_NODE:
                pass
            else:
                if child.nodeName == 'entity':
                    for value in child.childNodes:
                        if value.nodeType == child.TEXT_NODE:
                            if value.nodeName == 'type':
                                entity = {}
                                entity['type'] = value.data
                                entity['position'] = (i, j)
                                entity['properties'] = {}
                                self.addEntity(entity)


    def addEntity(self, entity):
        self.entities[entity.id] = entity
        self.getChunk(entity).addEntity(entity)

    def removeEntity(self, entity):     # 此处， 是否 entity的position 已经是新场景的position？
        del self.entities[entity.id]
        self.getChunk(entity).removeEntity(entity)

    def entityMove(self, entity, old_pos):
        if entity.position[0]/Space.CHUNK_WIDTH <> old_pos[0]/Space.CHUNK_WIDTH or \
            entity.position[1]/Space.CHUNK_HEIGHT <> old_pos[1]/Space.CHUNK_HEIGHT:
            self.getChunkByPos(old_chunk_pos).removeEntity(entity)
            self.getChunk(entity).addEntity(entity)
        self.getChunk(entity).broadcast(entity, Protocol.Position(entity))

    def getChunk(self, entity):
        return self.chunks.get([(entity.position[0]/Space.CHUNK_WIDTH, entity.position[1]/Space.CHUNK_HEIGHT)], NoneChunk())

    def getChunkByPos(self, pos):
        return self.chunks.get([(pos[0]/Space.CHUNK_WIDTH, pos[1]/Space.CHUNK_HEIGHT)], NoneChunk())

    def broadcast(self, entity, msg):
        for entity in self.entities:
            if isinstance(entity, Proxy):
                entity.talk(msg)
