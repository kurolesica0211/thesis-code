================================ System Message ================================

### Role
You are an expert Knowledge Graph Engineer. Your task is to update and refine a Data Graph based on a provided Input Text and a strict Ontology. You must ensure the Data Graph accurately reflects the information in the text while remaining compliant with the ontological constraints.

### Inputs
1. **Ontology**: Allowed classes and properties.
2. **Input Text**: The ONLY source of truth.
3. **Current Data Graph**: The starting state.

### Strict Grounding & Scope
- **No External Knowledge**: You are a "clean slate" engineer. Even if you know more about the subject from your training data, you MUST NOT add any node or relation that is not explicitly mentioned in the **Input Text**.
- **No Hypothetical Nodes**: Do not create placeholder nodes or sequences (e.g., Marriage1, Marriage2) to represent "patterns" mentioned in the text. Only create nodes for specific instances described.
- **Quantities**: If the text says "fifteen children" but does not name them, do NOT create 15 generic child nodes. Only create nodes for entities with specific names or identifiers provided in the text.

### Triadic Directionality & Predicate Logic (STRICT ENFORCEMENT)
The Data Graph is a **Directed Acyclic Graph**. Swapping Source and Target is a critical failure that invalidates the entire graph. You MUST follow the **Flow of Action**.

#### 1. The "Sentence Test" Requirement
Before executing any `AddTriple` call, you must mentally or explicitly (in your thought process) perform the following test:
* **Formula**: `[Source Entity] + [Property Name] + [Target Entity]`
* **Check**: Does this form a grammatically and logically correct sentence based *only* on the text?
* **Example Failure**: If the text says "John is the employer of Mary," the triple `(Mary, isEmployerOf, John)` fails because "Mary isEmployerOf John" is factually false.

#### 2. Identifying the Anchor (Domain vs. Range)
* **The Source**: The "Origin" or "Owner." If the property is a verb, the Source is the one performing it. Source is always to the left of a relation.
* **The Target**: The "Destination" or "Attribute." If the property is a verb, the Target is the one being acted upon. Target is always to the right of a relation.

#### 3. Handling Inverse Property Confusion
Many errors occur because the LLM confuses a relation with its inverse. You must be hyper-vigilant:
* **Active (`worksFor`, `isEmployerOf`)**: The "Superior" or "Source" is the Source.
* **Passive (`employedBy`, `childOf`)**: The "Subordinate" or "Recipient" is the Source.
* **Partitive (`hasPart`, `contains`)**: The "Container/Whole" is the Source.
* **Membership (`isPartOf`, `memberOf`)**: The "Component/Part" is the Source.

#### 4. Negative Constraints
* **NEVER** use the property name as a bidirectional link.
* **NEVER** assume the first entity mentioned in a sentence is automatically the Source; analyze the verb direction.

#### 5. Arguments Order
* When calling `AddTriple` `source` **ALWAYS** comes first, then `relation`, and only after them `target`.

> **STOP & VERIFY**: If your triple reads like "Employee isEmployerOf Employer" or "Room contains Building," you have flipped the nodes. **STOP and swap them before calling the tool.**


### Naming Conventions
- **Identifiers**: Use semantic identifiers derived from the text. 
- **Avoid Numbering**: Do not use arbitrary numbers unless that specific number appears in the text in relation to that entity.
- **Inclusion of Titles**: Retain all regnal numbers, honorary prefixes, or noble titles if they are part of the primary identifying name (e.g., "Crown Prince [Name]" or "[Name] II").
- **Territorial Origins**: If a person is identified by their house, dynasty, or place of origin as part of their formal name, include the full "of [Location]" or "[Location-Suffix]" descriptor.
- **Avoid Pronouns/Aliases**: Never use pronouns or shortened versions of the name mentioned later in the text. Always map back to the most complete version of the name found within the source material.

### Instructions & Workflow
1. **Analyze**: Identify specific entities and relations in the text.
2. **Edit**: Use tools to modify the graph.
   - Every node MUST have a class assignment (`AssignClass`).
   - Ground every edit in text evidence.
3. **Finalize**: Use `Finish` once the graph is a **faithful** representation of the text.

### Tool Usage Constraints
- **AssignClass / UnassignClass**: For `rdf:type` only.
- **AddTriple / RemoveTriple**: For properties only.
- **AddLiteral / RemoveLiteral**: For literals (raw data: dates, numbers, strings, etc.) only.
- **Finish**: Once you are finished, use this tool.
- **Batching**: You may use multiple tools, but **DON'T EXCEED 20 TOOL CALLS IN A SINGLE ANSWER**. Focus on quality and grounding over quantity.

================================ Human Message =================================

Please update the Knowledge Graph based on the provided data.

### Input Text:
Princess Alexandra of Greece and Denmark (Greek: Αλεξάνδρα; romanized: Alexándra), later known as Grand Duchess Alexandra Georgievna of Russia (Russian: Алекса́ндра Гео́ргиевна); 30 August  1870 – 24 September  1891), was a member of the Greek royal family by birth and of the Russian imperial family by marriage.
Alexandra was the daughter of George I of Greece and Olga Constantinovna of Russia, and grew up in Athens.
In 1889, she married Grand Duke Paul Alexandrovich of Russia, her first cousin once removed.
The couple settled in Saint Petersburg and they had two children: Grand Duchess Maria Pavlovna (1890–1958) and Grand Duke Dmitri Pavlovich (1891–1942).
Early life

Princess Alexandra of Greece and Denmark was born on 30 August  1870 at Mon Repos, the summer residence of the Greek royal family on the island of Corfu.
She was the third child and eldest daughter of King George I of Greece and his wife, Grand Duchess Olga Constantinovna of Russia.
Alexandra's father was not a native Greek, but he had been born a Danish prince named Christian Wilhelm of Schleswig-Holstein-Sonderburg-Glücksburg, a son of Christian IX, King of Denmark, and he had been elected to the Greek throne at the age of seventeen.
Five of his sons (Constantine, George, Nicholas, Andrew and Christopher), and two daughters (Alexandra and Maria), attained adulthood.
King George was a taciturn man, but contrary to the general approach of the time, he believed in happy rambunctious children.
The long corridors of the royal palace in Athens were used by Alexandra and her siblings for all types of play and sometimes a "bike ride" would be led by the King himself.
Alexandra, nicknamed "Aline" within her family, or Greek Alix, to distinguish her from her aunt and godmother, Alexandra, Princess of Wales, had a sunny disposition and was much loved by her family.
"


Alexandra's playmates were her brother Nicholas and her sister Maria, who followed her in age.
Alexandra spent many holidays in Denmark visiting her paternal grandparents.
In Denmark, Alexandra and her siblings met their Russian and British cousins in large family gatherings.
Marriage and children

When she was 18 years old, she was married to Grand Duke Paul Alexandrovich of Russia, her maternal first cousin once removed and the youngest child and sixth son of Emperor Alexander II and his first wife, Princess Marie of Hesse and by Rhine.
They had become close when Grand Duke Paul spent winters in Greece due to his frequent respiratory illnesses.
The Greek royal family also frequently spent holidays with the Romanov family on visits to Russia or Denmark.
They had two children:


Death

Seven months into her second pregnancy, Alexandra took a walk with her friends on the bank of the Moskva River and jumped directly into a boat that was permanently moored there, but fell as she got in.
The Grand Duchess was buried in the Peter and Paul Cathedral, St. Petersburg.
Her husband later morganatically remarried Olga Karnovich.
Alexandra's son would be involved in the murder of Grigori Rasputin, a friend of Tsarina Alexandra Feodorovna, in 1916.
In 1939 during the reign of her nephew George II of Greece, the Greek government obtained permission from the Soviet government under Joseph Stalin to rebury Princess Alexandra in Greece.
Alexandra's marble tombstone over an empty tomb is still in its place in the Peter and Paul Cathedral.
The "Alexandra Maternity Hospital" (now "Alexandra General Hospital") in Athens was later named in her memory by another nephew, King Paul; it was affiliated with the University of Athens with a special remit to research and combat postpartum maternal mortality.



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ns1: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
@prefix ns2: <http://www.w3.org/2003/11/swrl#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

: a owl:Ontology ;
    dcterms:source <http://www.co-ode.org/roberts/family-tree.owl> .

:alsoKnownAs a owl:AnnotationProperty .

:formerlyKnownAs a owl:AnnotationProperty .

:hasBirthYear a rdfs:Datatype,
        owl:AnnotationProperty .

:hasDeathYear a owl:AnnotationProperty .

:hasMarriageYear a owl:AnnotationProperty .

:isAuntOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    owl:propertyChainAxiom ( :isSisterOf :isParentOf ) .

:isUncleOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Person ;
    owl:propertyChainAxiom ( :isBrotherOf :isParentOf ) .

:knownAs a owl:AnnotationProperty .

dcterms:source a owl:AnnotationProperty .

ns1:isRuleEnabled a owl:AnnotationProperty .

:hasBrother a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Man ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:inverseOf :isBrotherOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:hasDaughter a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Woman ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf ;
    owl:inverseOf :isDaughterOf .

:hasFather a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Man ;
    rdfs:subPropertyOf :hasParent ;
    owl:inverseOf :isFatherOf .

:hasMother a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Woman ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf ;
    owl:inverseOf :isMotherOf .

:hasSister a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Woman ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:inverseOf :isSisterOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:hasSon a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Man ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf ;
    owl:inverseOf :isSonOf .

:isBloodrelationOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation,
        owl:topObjectProperty .

:isDaughterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf .

:isFatherOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor,
        :Man ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf .

:isMotherOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor,
        :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf .

:isSonOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf .

:DomainEntity a owl:Class .

:Female a owl:Class ;
    rdfs:subClassOf :Sex ;
    owl:disjointWith :Male .

:hasAncestor a owl:ObjectProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasRelation,
        owl:topObjectProperty ;
    owl:inverseOf :isAncestorOf .

:isBrotherOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:Male a owl:Class ;
    rdfs:subClassOf :Sex .

:hasRelation a owl:ObjectProperty,
        owl:SymmetricProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person .

:hasSex a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Sex .

:isAncestorOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation .

:isSisterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf .

:hasChild a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:inverseOf :isChildOf .

:hasParent a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Person ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:equivalentProperty :isChildOf ;
    owl:inverseOf :isParentOf .

:isSiblingOf a owl:ObjectProperty,
        owl:SymmetricProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isBloodrelationOf ;
    owl:propertyChainAxiom ( :hasParent :isParentOf ) .

:Sex a owl:Class ;
    rdfs:subClassOf :DomainEntity ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Female :Male ) ] .

:isChildOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:propertyDisjointWith :isSisterOf .

:x a ns2:Variable .

:Man a owl:Class ;
    owl:disjointWith :Sex,
        :Woman ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Male ] ) ] .

:isParentOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:propertyDisjointWith :isSisterOf .

:Woman a owl:Class ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Female ] ) ] .

:y a ns2:Variable .

:Ancestor a owl:Class ;
    owl:disjointWith :Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :isAncestorOf ;
                        owl:someValuesFrom :Person ] ) ] .

:Person a owl:Class ;
    rdfs:subClassOf [ a owl:Restriction ;
            owl:onProperty :hasFather ;
            owl:someValuesFrom :Man ],
        [ a owl:Restriction ;
            owl:onProperty :hasMother ;
            owl:someValuesFrom :Woman ],
        [ a owl:Restriction ;
            owl:onProperty :hasSex ;
            owl:someValuesFrom :Sex ],
        [ a owl:Restriction ;
            owl:maxQualifiedCardinality "2"^^xsd:nonNegativeInteger ;
            owl:onClass :Person ;
            owl:onProperty :hasParent ],
        :DomainEntity ;
    owl:disjointWith :Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Man :Woman ) ] .

[] a ns2:Imp ;
    rdfs:label "infer hasSon" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasBrother" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasSister" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (252b1f43-5a16-4861-b713-bdb280459a1f)
 Call ID: 252b1f43-5a16-4861-b713-bdb280459a1f
  Args:
    source: :Alexandra_of_Greece_and_Denmark
    type: :Woman
  AssignClass (7525d9c9-65b2-40c4-b8e0-ba6d6f5c7eaf)
 Call ID: 7525d9c9-65b2-40c4-b8e0-ba6d6f5c7eaf
  Args:
    source: :Alexandra_of_Greece_and_Denmark
    type: :Person
  AddLiteral (f4228f14-dd3c-4a92-8821-f5db85409b59)
 Call ID: f4228f14-dd3c-4a92-8821-f5db85409b59
  Args:
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1870
    source: :Alexandra_of_Greece_and_Denmark
  AddLiteral (2ecd6607-a18d-43b0-8738-62082946d03d)
 Call ID: 2ecd6607-a18d-43b0-8738-62082946d03d
  Args:
    literal_type: xsd:integer
    relation: :hasDeathYear
    literal_value: 1891
    source: :Alexandra_of_Greece_and_Denmark
  AddLiteral (6d2613cf-96d9-4ab6-ac85-8f12c63a7377)
 Call ID: 6d2613cf-96d9-4ab6-ac85-8f12c63a7377
  Args:
    relation: :alsoKnownAs
    literal_value: Alexandra Georgievna
    literal_type: xsd:string
    source: :Alexandra_of_Greece_and_Denmark
  AssignClass (d8d9c813-df14-40ea-94b7-9a86adcba71a)
 Call ID: d8d9c813-df14-40ea-94b7-9a86adcba71a
  Args:
    type: :Man
    source: :George_I_of_Greece
  AssignClass (8fcff825-9ca1-453b-87ab-688dc64f9b02)
 Call ID: 8fcff825-9ca1-453b-87ab-688dc64f9b02
  Args:
    type: :Person
    source: :George_I_of_Greece
  AssignClass (95c025cd-50b6-422e-a813-60efe4b93ca6)
 Call ID: 95c025cd-50b6-422e-a813-60efe4b93ca6
  Args:
    type: :Woman
    source: :Olga_Constantinovna_of_Russia
  AssignClass (59a5bee0-d488-490c-b050-d68451bdc82d)
 Call ID: 59a5bee0-d488-490c-b050-d68451bdc82d
  Args:
    type: :Person
    source: :Olga_Constantinovna_of_Russia
  AddTriple (f3b7dd2a-d507-4cc1-83c3-74ccf6f53ff1)
 Call ID: f3b7dd2a-d507-4cc1-83c3-74ccf6f53ff1
  Args:
    relation: :isFatherOf
    target: :Alexandra_of_Greece_and_Denmark
    source: :George_I_of_Greece
  AddTriple (9804109e-faac-44a2-b50f-3db223df08ed)
 Call ID: 9804109e-faac-44a2-b50f-3db223df08ed
  Args:
    relation: :isMotherOf
    target: :Alexandra_of_Greece_and_Denmark
    source: :Olga_Constantinovna_of_Russia
  AssignClass (ff41767e-7a5c-48b8-b8a0-be37f23545c2)
 Call ID: ff41767e-7a5c-48b8-b8a0-be37f23545c2
  Args:
    type: :Man
    source: :Paul_Alexandrovich_of_Russia
  AssignClass (e925513f-e743-48d9-920a-e5b4e8b24fa7)
 Call ID: e925513f-e743-48d9-920a-e5b4e8b24fa7
  Args:
    source: :Paul_Alexandrovich_of_Russia
    type: :Person
  AddLiteral (0ec7c12e-9fdc-4896-88d4-ea5cc338aa1b)
 Call ID: 0ec7c12e-9fdc-4896-88d4-ea5cc338aa1b
  Args:
    literal_type: xsd:integer
    literal_value: 1889
    relation: :hasMarriageYear
    source: :Alexandra_of_Greece_and_Denmark
  AddTriple (abd597de-5aef-4a1e-bcb5-3fa32a86476f)
 Call ID: abd597de-5aef-4a1e-bcb5-3fa32a86476f
  Args:
    relation: :hasRelation
    target: :Paul_Alexandrovich_of_Russia
    source: :Alexandra_of_Greece_and_Denmark
  AssignClass (e1cba178-88b1-4036-a46a-13cb2b29618c)
 Call ID: e1cba178-88b1-4036-a46a-13cb2b29618c
  Args:
    type: :Woman
    source: :Maria_Pavlovna
  AssignClass (34721d0d-cdb3-4638-b2cf-0e5cc4295d83)
 Call ID: 34721d0d-cdb3-4638-b2cf-0e5cc4295d83
  Args:
    type: :Person
    source: :Maria_Pavlovna
  AssignClass (f5e11493-6cc3-4e6b-83af-f8cb5fe86105)
 Call ID: f5e11493-6cc3-4e6b-83af-f8cb5fe86105
  Args:
    type: :Man
    source: :Dmitri_Pavlovich
  AssignClass (aa08420a-c844-4b15-841f-a97045d9ee38)
 Call ID: aa08420a-c844-4b15-841f-a97045d9ee38
  Args:
    type: :Person
    source: :Dmitri_Pavlovich
  AddTriple (f7a73e9e-0588-49de-8ab3-e8cf50247360)
 Call ID: f7a73e9e-0588-49de-8ab3-e8cf50247360
  Args:
    source: :Maria_Pavlovna
    target: :Alexandra_of_Greece_and_Denmark
    relation: :isChildOf
  AddTriple (040e7c90-c316-4662-8e0b-883d8290f59e)
 Call ID: 040e7c90-c316-4662-8e0b-883d8290f59e
  Args:
    target: :Paul_Alexandrovich_of_Russia
    relation: :isChildOf
    source: :Maria_Pavlovna
  AddTriple (05257df0-669b-47b6-8d2b-1d9301f37d94)
 Call ID: 05257df0-669b-47b6-8d2b-1d9301f37d94
  Args:
    source: :Dmitri_Pavlovich
    relation: :isChildOf
    target: :Alexandra_of_Greece_and_Denmark
  AddTriple (7d467a62-1e3d-48c3-b578-6bca93750a22)
 Call ID: 7d467a62-1e3d-48c3-b578-6bca93750a22
  Args:
    source: :Dmitri_Pavlovich
    target: :Paul_Alexandrovich_of_Russia
    relation: :isChildOf
  AssignClass (7a6f1d06-7643-43aa-b3b7-707a2ba66480)
 Call ID: 7a6f1d06-7643-43aa-b3b7-707a2ba66480
  Args:
    type: :Man
    source: :Nicholas_of_Greece
  AssignClass (649a594b-6539-4a5c-b26f-42f1f471d449)
 Call ID: 649a594b-6539-4a5c-b26f-42f1f471d449
  Args:
    source: :Nicholas_of_Greece
    type: :Person
  AssignClass (78f2ad75-6497-4b3d-b76d-18c3be718657)
 Call ID: 78f2ad75-6497-4b3d-b76d-18c3be718657
  Args:
    source: :Maria_of_Greece
    type: :Woman
  AssignClass (ac4abae4-6a8b-4fff-bf11-f2942aa60d5a)
 Call ID: ac4abae4-6a8b-4fff-bf11-f2942aa60d5a
  Args:
    type: :Person
    source: :Maria_of_Greece
  AddTriple (0738e3f7-4d72-4d64-b779-debd95f8a9a7)
 Call ID: 0738e3f7-4d72-4d64-b779-debd95f8a9a7
  Args:
    target: :Nicholas_of_Greece
    relation: :isSiblingOf
    source: :Alexandra_of_Greece_and_Denmark
  AddTriple (a374e1cd-d886-4014-ab99-5f2d003d6f41)
 Call ID: a374e1cd-d886-4014-ab99-5f2d003d6f41
  Args:
    relation: :isSiblingOf
    target: :Maria_of_Greece
    source: :Alexandra_of_Greece_and_Denmark
  AssignClass (9cacb534-dc13-4a87-87c9-bbe9c462790f)
 Call ID: 9cacb534-dc13-4a87-87c9-bbe9c462790f
  Args:
    source: :Christian_IX_of_Denmark
    type: :Man
  AssignClass (a61fdbf6-6cf4-473b-80fa-9b7694eaac65)
 Call ID: a61fdbf6-6cf4-473b-80fa-9b7694eaac65
  Args:
    source: :Christian_IX_of_Denmark
    type: :Person
  AddTriple (7f016aec-d74a-406d-bfbf-a5928bafc255)
 Call ID: 7f016aec-d74a-406d-bfbf-a5928bafc255
  Args:
    relation: :isFatherOf
    target: :George_I_of_Greece
    source: :Christian_IX_of_Denmark
  AssignClass (b1b35a53-30a0-42c5-9ef8-c9e2fb03fcd0)
 Call ID: b1b35a53-30a0-42c5-9ef8-c9e2fb03fcd0
  Args:
    source: :Alexander_II_of_Russia
    type: :Man
  AssignClass (c306e181-2dff-41a1-9797-6fc4a6af4fe5)
 Call ID: c306e181-2dff-41a1-9797-6fc4a6af4fe5
  Args:
    type: :Person
    source: :Alexander_II_of_Russia
  AssignClass (b9f73a73-a32f-4fe8-9110-2aee8baab769)
 Call ID: b9f73a73-a32f-4fe8-9110-2aee8baab769
  Args:
    type: :Woman
    source: :Marie_of_Hesse_and_by_Rhine
  AssignClass (1f0929c6-d194-4a63-811d-821560057b07)
 Call ID: 1f0929c6-d194-4a63-811d-821560057b07
  Args:
    source: :Marie_of_Hesse_and_by_Rhine
    type: :Person
  AddTriple (10128afb-e216-43f3-9a2f-f2520aeffe1d)
 Call ID: 10128afb-e216-43f3-9a2f-f2520aeffe1d
  Args:
    relation: :isFatherOf
    target: :Paul_Alexandrovich_of_Russia
    source: :Alexander_II_of_Russia
  AddTriple (96c3f7ee-b53e-4b3c-a1ad-f72c524dc0f8)
 Call ID: 96c3f7ee-b53e-4b3c-a1ad-f72c524dc0f8
  Args:
    target: :Paul_Alexandrovich_of_Russia
    relation: :isMotherOf
    source: :Marie_of_Hesse_and_by_Rhine
  AssignClass (565a9c18-03c0-45f0-87c7-ea1240577956)
 Call ID: 565a9c18-03c0-45f0-87c7-ea1240577956
  Args:
    type: :Woman
    source: :Olga_Karnovich
  AssignClass (c74a9843-96f9-43bd-b27a-9e9117260876)
 Call ID: c74a9843-96f9-43bd-b27a-9e9117260876
  Args:
    type: :Person
    source: :Olga_Karnovich
  AddTriple (eee2faf5-858f-4b11-9174-7e809d898282)
 Call ID: eee2faf5-858f-4b11-9174-7e809d898282
  Args:
    source: :Paul_Alexandrovich_of_Russia
    relation: :hasRelation
    target: :Olga_Karnovich
  AssignClass (38481b75-3210-48aa-ad93-9e6a1edd0f2f)
 Call ID: 38481b75-3210-48aa-ad93-9e6a1edd0f2f
  Args:
    source: :George_II_of_Greece
    type: :Man
  AssignClass (4edd0ffc-f607-4454-9367-be1e9dda9f5c)
 Call ID: 4edd0ffc-f607-4454-9367-be1e9dda9f5c
  Args:
    type: :Person
    source: :George_II_of_Greece
  AssignClass (7590e594-bed1-4611-8f8b-b0da12c4511e)
 Call ID: 7590e594-bed1-4611-8f8b-b0da12c4511e
  Args:
    type: :Man
    source: :Paul_of_Greece
  AssignClass (53996ed1-9ef1-4d63-8658-aa82561bfb30)
 Call ID: 53996ed1-9ef1-4d63-8658-aa82561bfb30
  Args:
    type: :Person
    source: :Paul_of_Greece
  Finish (60cf0660-401d-41f9-b769-d8b3ecd43bf4)
 Call ID: 60cf0660-401d-41f9-b769-d8b3ecd43bf4
  Args: