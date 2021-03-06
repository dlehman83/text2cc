# -*- coding: utf-8 -*-
#
# Copyright (c) 2021, Dana Lehman
# Copyright (c) 2020, Geoffrey M. Poore
# All rights reserved.
#
# Licensed under the BSD 3-Clause License:
# http://opensource.org/licenses/BSD-3-Clause
#


import io
import pathlib
from typing import Union, BinaryIO
import zipfile
from .quiz import Quiz
from .xml_imsmanifest import imsmanifest
from .xml_assessment import assessment


class QTI(object):
    '''
    Create QTI from a Quiz object.
    '''
    def __init__(self, quiz: Quiz):
        self.quiz = quiz
        id_base = 'text2cc'
        self.manifest_identifier = f'{id_base}_manifest_{quiz.id}'
        self.assessment_identifier = f'{id_base}_assessment_{quiz.id}'
        self.dependency_identifier = f'{id_base}_dependency_{quiz.id}'
        self.assignment_identifier = f'{id_base}_assignment_{quiz.id}'
        self.assignment_group_identifier = f'{id_base}_assignment-group_{quiz.id}'

        self.imsmanifest_xml = imsmanifest(manifest_identifier=self.manifest_identifier,
                                           assessment_identifier=self.assessment_identifier,
                                           dependency_identifier=self.dependency_identifier,
                                           title_xml=quiz.title_xml,
                                           images=self.quiz.images)
        
        self.assessment = assessment(quiz=quiz,
                                     assessment_identifier=self.assessment_identifier,
                                     title_xml=quiz.title_xml)


    def write(self, bytes_stream: BinaryIO):
        with zipfile.ZipFile(bytes_stream, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
            zf.writestr('imsmanifest.xml', self.imsmanifest_xml)
            #zf.writestr(zipfile.ZipInfo('non_cc_assessments/'), b'')
            
            zf.writestr(f'{self.assessment_identifier}/{self.assessment_identifier}.xml', self.assessment)
            for image in self.quiz.images.values():
                zf.writestr(image.qti_zip_path, image.data)


    def zip_bytes(self) -> bytes:
        stream = io.BytesIO()
        self.write(stream)
        return stream.getvalue()


    def save(self, qti_path: Union[str, pathlib.Path]):
        if isinstance(qti_path, str):
            qti_path = pathlib.Path(qti_path)
        elif not isinstance(qti_path, pathlib.Path):
            raise TypeError
        qti_path.write_bytes(self.zip_bytes())
