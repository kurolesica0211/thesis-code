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
Duke Adolf Friedrich Albrecht Heinrich of Mecklenburg-Schwerin (German: Adolf Friedrich Albrecht Heinrich, Herzog zu Mecklenburg-Schwerin; 10 October 1873 – 5 August 1969), was a German explorer in Africa, a colonial politician,  and the first president of the National Olympic Committee of West Germany (1949–1951).
Biography

Born in Schwerin, Adolf Friedrich was the third child of Frederick Francis II, Grand Duke of Mecklenburg-Schwerin (1823–1883), and his third wife Princess Marie of Schwarzburg-Rudolstadt.
Explorer of Africa

From 1907 to 1908, Adolf Friedrich led a scientific research expedition in the region of the Central African Graben and traversed  Africa from east to west.
Adolf Friedrich and his companions explored the then little-known primeval forest region of the Congo tributaries and the basin of Lake Chad.
From 1912 to 1914, Adolf Friedrich was the last governor of Togoland in German West Africa; he was invited for the official celebration of the independence of Togo in 1960.
Duke candidate for the planned United Baltic Duchy

At the end of the First World War, in the autumn of 1918, the Duke was offered the throne of the United Baltic Duchy, a short-lived client-state proclaimed on Baltic territories under German occupation.
By the autumn of 1918, the Duke was approached by Heinrich von Stryk, a representative of the Baltic German nobility, but final steps towards implementation of their plans were undertaken on 5 November, when representatives of Baltic Germans and some pro-German oriented leaders among Estonian and Latvian politicians from Courland, Livonia and Estonia met in Riga and proclaimed the creation of the United Baltic Duchy.
Since the Duke was in Germany, the temporary regency council (Regentschaftsrat) was established in Riga, headed by baron Adolf Pilar von Pilchau, and consisting of three Baltic Germans, three Estonians and three Latvians.
Since Germany lost the War by 11 November, the Duke never assumed the Baltic throne.
Member of the International Olympic Committee

Adolf Friedrich then served as a member of the International Olympic Committee from 1926 to 1956 and as the first president of the National Olympic Committee of Germany from 1949 to 1951.
Personal life

Adolf Friedrich was married twice.
In Gera on 24 April 1917, he married Princess Viktoria Feodora of Reuss-Schleiz (1889-1918), daughter of Heinrich XXVII, Prince Reuss Younger Line and Princess Elise of Hohenlohe-Langenburg.
He later married the widow of his half-brother Duke John Albert, Princess Elisabeth of Stolberg-Rossla, on 15 October 1924; they were among the guests at 
the 1937 wedding of Juliana of the Netherlands and Prince Bernhard of Lippe-Biesterfeld.
Princess Elisabeth survived her husband by only a few weeks after his death in Eutin in 1969.
Legacy

Adolf Friedrich is commemorated in the scientific names of a genus of lizards, Adolfus, and of a species of chameleon, Kinyongia adolfifriderici, as well as in the cichlid Haplochromis adolphifrederici, and in the large tree species Aningeria adolfi-friederici.



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
  AssignClass (cb068df8-1516-4dee-8988-91d7078c5239)
 Call ID: cb068df8-1516-4dee-8988-91d7078c5239
  Args:
    type: :Man
    source: Adolf_Friedrich
  AssignClass (081766ae-cae3-452e-a2e6-11459c64d571)
 Call ID: 081766ae-cae3-452e-a2e6-11459c64d571
  Args:
    type: :Person
    source: Adolf_Friedrich
  AddLiteral (9d812f26-89a9-485b-b382-8ee8b542f4ea)
 Call ID: 9d812f26-89a9-485b-b382-8ee8b542f4ea
  Args:
    literal_value: 1873
    source: Adolf_Friedrich
    literal_type: xsd:positiveInteger
    relation: :hasBirthYear
  AddLiteral (25e2c639-dc03-43f9-85c5-ac62dffe7deb)
 Call ID: 25e2c639-dc03-43f9-85c5-ac62dffe7deb
  Args:
    literal_type: xsd:positiveInteger
    relation: :hasDeathYear
    literal_value: 1969
    source: Adolf_Friedrich
  AssignClass (9575b06d-94f2-43db-aab7-e8656f7ef831)
 Call ID: 9575b06d-94f2-43db-aab7-e8656f7ef831
  Args:
    type: :Man
    source: Frederick_Francis_II
  AssignClass (df144f07-a896-46a7-8773-fa75240fcb5a)
 Call ID: df144f07-a896-46a7-8773-fa75240fcb5a
  Args:
    type: :Person
    source: Frederick_Francis_II
  AddLiteral (a80efdf1-5acd-4a5f-bf53-9e39c43879e3)
 Call ID: a80efdf1-5acd-4a5f-bf53-9e39c43879e3
  Args:
    literal_value: 1823
    source: Frederick_Francis_II
    literal_type: xsd:positiveInteger
    relation: :hasBirthYear
  AddLiteral (f03d9896-9c03-4bae-b5aa-5f5c7f2bfd82)
 Call ID: f03d9896-9c03-4bae-b5aa-5f5c7f2bfd82
  Args:
    literal_value: 1883
    source: Frederick_Francis_II
    literal_type: xsd:positiveInteger
    relation: :hasDeathYear
  AssignClass (a8c397ec-a939-4da8-9f6c-a61f727ee0b2)
 Call ID: a8c397ec-a939-4da8-9f6c-a61f727ee0b2
  Args:
    type: :Woman
    source: Marie_of_Schwarzburg-Rudolstadt
  AssignClass (dd983af6-c9d7-4f8d-9bd8-82a5cf0da672)
 Call ID: dd983af6-c9d7-4f8d-9bd8-82a5cf0da672
  Args:
    type: :Person
    source: Marie_of_Schwarzburg-Rudolstadt
  AddTriple (4302bd78-977b-41b2-92e8-602c8d591678)
 Call ID: 4302bd78-977b-41b2-92e8-602c8d591678
  Args:
    relation: :hasFather
    source: Adolf_Friedrich
    target: Frederick_Francis_II
  AddTriple (d90219e7-785b-4392-bf3e-95750b2b1a60)
 Call ID: d90219e7-785b-4392-bf3e-95750b2b1a60
  Args:
    relation: :hasMother
    target: Marie_of_Schwarzburg-Rudolstadt
    source: Adolf_Friedrich
  AssignClass (2b8d3868-e692-479e-b568-eb89e1310758)
 Call ID: 2b8d3868-e692-479e-b568-eb89e1310758
  Args:
    type: :Woman
    source: Viktoria_Feodora_of_Reuss-Schleiz
  AssignClass (d7ff65dd-9546-4b9b-b9b9-11f7d4412ce5)
 Call ID: d7ff65dd-9546-4b9b-b9b9-11f7d4412ce5
  Args:
    type: :Person
    source: Viktoria_Feodora_of_Reuss-Schleiz
  AddLiteral (e77a6d7d-1708-4616-9e0a-acd9040cd1ee)
 Call ID: e77a6d7d-1708-4616-9e0a-acd9040cd1ee
  Args:
    relation: :hasMarriageYear
    literal_type: xsd:positiveInteger
    source: Adolf_Friedrich
    literal_value: 1917
  AssignClass (8a572c79-b012-4511-ae0a-f4ca074b1a15)
 Call ID: 8a572c79-b012-4511-ae0a-f4ca074b1a15
  Args:
    type: :Man
    source: Heinrich_XXVII_Prince_Reuss_Younger_Line
  AssignClass (5d8f48fa-8696-49ab-b2c4-51227b38fbad)
 Call ID: 5d8f48fa-8696-49ab-b2c4-51227b38fbad
  Args:
    type: :Person
    source: Heinrich_XXVII_Prince_Reuss_Younger_Line
  AssignClass (97d183c0-6ce6-47b0-9997-91446e5dd800)
 Call ID: 97d183c0-6ce6-47b0-9997-91446e5dd800
  Args:
    type: :Woman
    source: Elise_of_Hohenlohe-Langenburg
  AssignClass (300250d5-94f9-4d7e-b779-c4a5c175f423)
 Call ID: 300250d5-94f9-4d7e-b779-c4a5c175f423
  Args:
    type: :Person
    source: Elise_of_Hohenlohe-Langenburg
  AddTriple (563826bf-4f80-4e96-84cd-7dfafa57bd68)
 Call ID: 563826bf-4f80-4e96-84cd-7dfafa57bd68
  Args:
    relation: :hasFather
    target: Heinrich_XXVII_Prince_Reuss_Younger_Line
    source: Viktoria_Feodora_of_Reuss-Schleiz
  AddTriple (bee85cde-0c12-45d7-9e8a-4a235fe7bc6d)
 Call ID: bee85cde-0c12-45d7-9e8a-4a235fe7bc6d
  Args:
    relation: :hasMother
    target: Elise_of_Hohenlohe-Langenburg
    source: Viktoria_Feodora_of_Reuss-Schleiz
  AssignClass (428f8f56-d760-43ce-8811-75b4039fafaa)
 Call ID: 428f8f56-d760-43ce-8811-75b4039fafaa
  Args:
    type: :Man
    source: John_Albert
  AssignClass (736668ae-8579-4312-a2ef-1bb268116f88)
 Call ID: 736668ae-8579-4312-a2ef-1bb268116f88
  Args:
    type: :Person
    source: John_Albert
  AssignClass (15e6698b-d9ed-4da6-b10c-919b5bb83211)
 Call ID: 15e6698b-d9ed-4da6-b10c-919b5bb83211
  Args:
    type: :Woman
    source: Elisabeth_of_Stolberg-Rossla
  AssignClass (5e9c9896-bbc0-49d3-99b6-e24375ed45c7)
 Call ID: 5e9c9896-bbc0-49d3-99b6-e24375ed45c7
  Args:
    type: :Person
    source: Elisabeth_of_Stolberg-Rossla
  AddTriple (4cb1943e-6bd2-4f4d-86ab-2c7ecd0237db)
 Call ID: 4cb1943e-6bd2-4f4d-86ab-2c7ecd0237db
  Args:
    target: Adolf_Friedrich
    source: John_Albert
    relation: :isBrotherOf
  AddLiteral (5cdb397c-90d6-4d03-b89b-3bb085cd867b)
 Call ID: 5cdb397c-90d6-4d03-b89b-3bb085cd867b
  Args:
    literal_type: xsd:positiveInteger
    relation: :hasMarriageYear
    literal_value: 1924
    source: Adolf_Friedrich
  Finish (e6e741ae-4438-4c4c-88a5-4e1f48512360)
 Call ID: e6e741ae-4438-4c4c-88a5-4e1f48512360
  Args: