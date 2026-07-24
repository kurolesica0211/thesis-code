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
The Custodian of the Crown  Prince Radu


Princess Elena 
Princess Irina 
Princess Sophie 
Princess Maria 


Princess Maria of Romania (born 13 July 1964) is the fifth and youngest daughter of King Michael I and Queen Anne of Romania.
Since 2015 Maria has lived in Romania and carried out a public role on behalf of the Romanian royal family.
Early life

Maria was born on 13 July 1964 at Copenhagen University Hospital Gentofte in Gentofte, Copenhagen, Denmark as the youngest of five daughters of King Michael I and Queen Anne.
Maria was born while her father was in the United States on business for the New York Stock Exchange.
Michael was informed by telephone that he'd become a father for the fifth time.
Maria was baptised by the Orthodox Church, with her eldest sister, Princess Margareta, as godmother.
Queen Marie, her paternal great-grandmother, was her namesake.
As a young girl, Maria and her sisters were told "fascinating tales of a homeland they couldn't visit" by their father.
Maria was educated at public school Rydal Penrhos (then Penrhos College) and in Switzerland where the family lived during exile, and spent most her early adult life living and working in the United States, including New York and New Mexico.
Careers

Maria's teenage years were spent in Switzerland with her family, where she received her primary and secondary education.
After completing her studies, Maria worked briefly in the childcare field.
After Maria's brief career in childcare, she pursued a career in New York, doing public relations for private companies.
When the situation in Romania eventually calmed down she left her public relations career and moved to New Mexico where she worked in private consulting until she moved to Romania in 2015.
Activities in Romania

Maria visited Romania with her parents and other members of the family in 1997, and from this point onwards began visiting the country regularly for Christmas or family events such as her parents' 60th Wedding Anniversary and King Michael's 90th Birthday celebrations.
On 7 May 2014, Maria was invested with the Grand Cross of the Order of the Crown in a ceremony conducted by Crown Princess Margareta at the Elisabeta Palace to mark Maria's upcoming 50th birthday.
This was followed by a dinner at the Palace attended by the Prime Minister of Romania (Victor Ponta) and other guests.
On 21 April 2015 it was announced by the Romanian cosmetic company Farmec that Maria is an official ambassador of the company, where she will participate in projects to promote products created in the research lab of the company, as well as social responsibility activities undertaken by Farmec.
In January 2015 it was announced that Maria would move to Romania permanently to take on activities in support of the royal family, and she was present in the public commemorations in Bucharest of 25 years since the royal family's return later the same month.
Maria has represented the royal family at events across the country, acted in support of Margareta, Custodian of the Crown and taken on a number of patronages including Concordia Humanitarian Organisation.
During her father's illnesses, Maria and her elder sisters took turns to be with him at his home in Switzerland and it was during her stay that King Michael died.
Marriage and divorce

On 16 September 1995, Maria married Kazimierz Wiesław Mystkowski (b. 13 September 1958 in Łaś-Toczyłowo), a Polish nobleman from the Mystkowski family and a computer engineer.
The wedding celebration was held at the Greek Orthodox Holy Trinity Cathedral in New York, and was attended by the Romanian royal family, the parents of Kazimierz, the newly married Crown Prince and Crown Princess of Greece.
King Michael I served as the couple's koumbaros (the best man who, during a Greek Orthodox wedding, exchanges the crowns over the couple’s heads).
In December 2003, the couple subsequently divorced without producing any children.


Legal issues

In July 2005, the princess was sued by her landlord, Donald Yates.
During this court case, her name was given as "Mia Mystkowski."
The next legal dispute in which the princess became entangled involved her HOA, the Sierra Madre Homeowners Association.
On 5 December 2008, the homeowner's association filed a general civil complaint against "Marie de Roumanie"; this was followed the next day by a civil summons being issued to the princess.
On 12 January 2009, Princess Maria of Romania was booked in Santa Fe County, New Mexico, on the charge of "failure to appear."
The princess was released the same day on a $200.00 bond.



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ns1: <http://www.w3.org/2003/11/swrl#> .
@prefix ns2: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
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

ns2:isRuleEnabled a owl:AnnotationProperty .

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

:x a ns1:Variable .

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

:y a ns1:Variable .

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

[] a ns1:Imp ;
    rdfs:label "infer hasSon" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasBrother" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasSister" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (46186077-beff-4d3b-99d7-7c48ccb04640)
 Call ID: 46186077-beff-4d3b-99d7-7c48ccb04640
  Args:
    type: :Person
    source: Princess_Maria_of_Romania
  AssignClass (6b998a34-44be-4c88-a5ad-06bb8ba24e3e)
 Call ID: 6b998a34-44be-4c88-a5ad-06bb8ba24e3e
  Args:
    type: :Woman
    source: Princess_Maria_of_Romania
  AssignClass (5804d121-3411-4180-aa97-9c73f5cd52f6)
 Call ID: 5804d121-3411-4180-aa97-9c73f5cd52f6
  Args:
    type: :Person
    source: King_Michael_I
  AssignClass (e36eadd2-dbed-4712-a401-28cf8868aa56)
 Call ID: e36eadd2-dbed-4712-a401-28cf8868aa56
  Args:
    type: :Man
    source: King_Michael_I
  AssignClass (4f0c37ff-aaca-4a66-938c-4cddd8577314)
 Call ID: 4f0c37ff-aaca-4a66-938c-4cddd8577314
  Args:
    type: :Ancestor
    source: King_Michael_I
  AssignClass (62092728-7839-47d0-9295-9d099ce8518c)
 Call ID: 62092728-7839-47d0-9295-9d099ce8518c
  Args:
    type: :Person
    source: Queen_Anne_of_Romania
  AssignClass (21572740-878b-4fc7-a7d6-f7ad27eb0a09)
 Call ID: 21572740-878b-4fc7-a7d6-f7ad27eb0a09
  Args:
    type: :Woman
    source: Queen_Anne_of_Romania
  AssignClass (835dd7ba-5e6b-4013-8ecc-bfff1039997a)
 Call ID: 835dd7ba-5e6b-4013-8ecc-bfff1039997a
  Args:
    type: :Ancestor
    source: Queen_Anne_of_Romania
  AddLiteral (195ba04b-f7bf-4e87-96fc-68024b9c4bfc)
 Call ID: 195ba04b-f7bf-4e87-96fc-68024b9c4bfc
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    literal_value: 1964
    source: Princess_Maria_of_Romania
  AddTriple (0c0ee971-7c40-4572-bd79-eeed41223acb)
 Call ID: 0c0ee971-7c40-4572-bd79-eeed41223acb
  Args:
    target: King_Michael_I
    relation: :hasFather
    source: Princess_Maria_of_Romania
  AddTriple (3b6b4c65-125c-4eec-9a03-525b45873f15)
 Call ID: 3b6b4c65-125c-4eec-9a03-525b45873f15
  Args:
    relation: :hasMother
    source: Princess_Maria_of_Romania
    target: Queen_Anne_of_Romania
  AddTriple (8662aaf1-ba0f-4f9d-8bf1-840d7be6b879)
 Call ID: 8662aaf1-ba0f-4f9d-8bf1-840d7be6b879
  Args:
    target: Princess_Margareta
    relation: :hasSister
    source: Princess_Maria_of_Romania
  AddTriple (41308959-0c57-4a56-885b-a6735b665b58)
 Call ID: 41308959-0c57-4a56-885b-a6735b665b58
  Args:
    relation: :hasSister
    source: Princess_Maria_of_Romania
    target: Princess_Elena
  AddTriple (b2492a08-d6fe-449a-877a-7440b4e0fb17)
 Call ID: b2492a08-d6fe-449a-877a-7440b4e0fb17
  Args:
    target: Princess_Irina
    relation: :hasSister
    source: Princess_Maria_of_Romania
  AddTriple (87336019-6484-4eb8-8f37-1d7a5badeaad)
 Call ID: 87336019-6484-4eb8-8f37-1d7a5badeaad
  Args:
    relation: :hasSister
    source: Princess_Maria_of_Romania
    target: Princess_Sophie
  AssignClass (a09bb722-159d-43b8-a395-7f71256c36f1)
 Call ID: a09bb722-159d-43b8-a395-7f71256c36f1
  Args:
    type: :Person
    source: Princess_Margareta
  AssignClass (bb7964ef-dfc3-4945-821f-cff317f4c0f5)
 Call ID: bb7964ef-dfc3-4945-821f-cff317f4c0f5
  Args:
    type: :Woman
    source: Princess_Margareta
  AssignClass (618ba821-561e-43a9-b291-f639be6fe74d)
 Call ID: 618ba821-561e-43a9-b291-f639be6fe74d
  Args:
    type: :Person
    source: Princess_Elena
  AssignClass (1530bbe5-ae5e-4b4c-8a2a-d620744e52cd)
 Call ID: 1530bbe5-ae5e-4b4c-8a2a-d620744e52cd
  Args:
    type: :Woman
    source: Princess_Elena
  AssignClass (1af6db5e-af70-4f56-8f29-cf8e0ac9bbd3)
 Call ID: 1af6db5e-af70-4f56-8f29-cf8e0ac9bbd3
  Args:
    type: :Person
    source: Princess_Irina
  AssignClass (37fe24ef-817b-4e8c-ab3a-3e99275a5ac7)
 Call ID: 37fe24ef-817b-4e8c-ab3a-3e99275a5ac7
  Args:
    type: :Woman
    source: Princess_Irina
  AssignClass (439685b1-65f0-4a59-bb74-6df671a17b28)
 Call ID: 439685b1-65f0-4a59-bb74-6df671a17b28
  Args:
    type: :Person
    source: Princess_Sophie
  AssignClass (a27aceae-2eea-4d6c-b2c4-3fe744a51550)
 Call ID: a27aceae-2eea-4d6c-b2c4-3fe744a51550
  Args:
    type: :Woman
    source: Princess_Sophie
  AssignClass (c8e39d71-6e06-48c6-9d04-54074748d21d)
 Call ID: c8e39d71-6e06-48c6-9d04-54074748d21d
  Args:
    type: :Person
    source: Kazimierz_Wiesław_Mystkowski
  AssignClass (066b0b82-4868-4461-8b3d-bad8aa8766a1)
 Call ID: 066b0b82-4868-4461-8b3d-bad8aa8766a1
  Args:
    type: :Man
    source: Kazimierz_Wiesław_Mystkowski
  AddLiteral (b3412841-60cc-49dc-a612-6b408cf72e90)
 Call ID: b3412841-60cc-49dc-a612-6b408cf72e90
  Args:
    source: Princess_Maria_of_Romania
    relation: :hasMarriageYear
    literal_value: 1995
    literal_type: xsd:integer
  AddTriple (c89a7ce6-e516-4a3b-b4c9-ac0607b68fe2)
 Call ID: c89a7ce6-e516-4a3b-b4c9-ac0607b68fe2
  Args:
    target: Kazimierz_Wiesław_Mystkowski
    relation: :hasRelation
    source: Princess_Maria_of_Romania
  AddLiteral (7769e5be-d60a-439b-bda3-6ca62ae499d6)
 Call ID: 7769e5be-d60a-439b-bda3-6ca62ae499d6
  Args:
    literal_type: xsd:string
    literal_value: Mia Mystkowski
    relation: :alsoKnownAs
    source: Princess_Maria_of_Romania
  AddLiteral (db95ad60-2b09-4222-ae7d-46bf2a26ca88)
 Call ID: db95ad60-2b09-4222-ae7d-46bf2a26ca88
  Args:
    relation: :alsoKnownAs
    literal_value: Marie de Roumanie
    literal_type: xsd:string
    source: Princess_Maria_of_Romania
  Finish (b3ee289f-ef7a-4524-88b8-3bbc54174e34)
 Call ID: b3ee289f-ef7a-4524-88b8-3bbc54174e34
  Args: