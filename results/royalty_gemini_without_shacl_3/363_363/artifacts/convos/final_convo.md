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
  AssignClass (bc94e441-ba3c-4d4b-9e28-e3eadb1086f8)
 Call ID: bc94e441-ba3c-4d4b-9e28-e3eadb1086f8
  Args:
    type: :Man
    source: Adolf_Friedrich_of_Mecklenburg-Schwerin
  AssignClass (d6b35b8c-d2a3-4196-844d-d9f2939eb39a)
 Call ID: d6b35b8c-d2a3-4196-844d-d9f2939eb39a
  Args:
    type: :Person
    source: Adolf_Friedrich_of_Mecklenburg-Schwerin
  AddLiteral (2a467c22-0335-4ba4-a9f3-6d9405e7ff50)
 Call ID: 2a467c22-0335-4ba4-a9f3-6d9405e7ff50
  Args:
    source: Adolf_Friedrich_of_Mecklenburg-Schwerin
    literal_type: xsd:integer
    relation: :hasBirthYear
    literal_value: 1873
  AddLiteral (32d9f8f4-5ba7-4f71-a4c8-224d1b87b107)
 Call ID: 32d9f8f4-5ba7-4f71-a4c8-224d1b87b107
  Args:
    literal_type: xsd:integer
    source: Adolf_Friedrich_of_Mecklenburg-Schwerin
    literal_value: 1969
    relation: :hasDeathYear
  AssignClass (bcf4cd52-5f9d-457d-ba8a-ac1af6066091)
 Call ID: bcf4cd52-5f9d-457d-ba8a-ac1af6066091
  Args:
    type: :Man
    source: Frederick_Francis_II_of_Mecklenburg-Schwerin
  AssignClass (73329bd2-d852-4caf-8a3e-88fcec4e7e6d)
 Call ID: 73329bd2-d852-4caf-8a3e-88fcec4e7e6d
  Args:
    type: :Person
    source: Frederick_Francis_II_of_Mecklenburg-Schwerin
  AssignClass (60f44281-06cf-4095-be66-baa82f9762fd)
 Call ID: 60f44281-06cf-4095-be66-baa82f9762fd
  Args:
    type: :Ancestor
    source: Frederick_Francis_II_of_Mecklenburg-Schwerin
  AddLiteral (e2acfc91-b996-4231-b5d1-8994d8a5a103)
 Call ID: e2acfc91-b996-4231-b5d1-8994d8a5a103
  Args:
    literal_type: xsd:integer
    source: Frederick_Francis_II_of_Mecklenburg-Schwerin
    literal_value: 1823
    relation: :hasBirthYear
  AddLiteral (65fc0b2e-9c12-43b3-89e8-d7a40ccf6fa3)
 Call ID: 65fc0b2e-9c12-43b3-89e8-d7a40ccf6fa3
  Args:
    literal_value: 1883
    relation: :hasDeathYear
    literal_type: xsd:integer
    source: Frederick_Francis_II_of_Mecklenburg-Schwerin
  AssignClass (7f9c3f30-2be6-4fe6-b57d-1dce5beea7fe)
 Call ID: 7f9c3f30-2be6-4fe6-b57d-1dce5beea7fe
  Args:
    type: :Woman
    source: Marie_of_Schwarzburg-Rudolstadt
  AssignClass (49249008-3aa4-4be5-86eb-13cfa0b82077)
 Call ID: 49249008-3aa4-4be5-86eb-13cfa0b82077
  Args:
    type: :Person
    source: Marie_of_Schwarzburg-Rudolstadt
  AssignClass (ee7914de-ea0d-450f-a95f-4c944bf67369)
 Call ID: ee7914de-ea0d-450f-a95f-4c944bf67369
  Args:
    type: :Ancestor
    source: Marie_of_Schwarzburg-Rudolstadt
  AddTriple (ad574e9e-44a4-40a3-83cb-d5414d76e1d2)
 Call ID: ad574e9e-44a4-40a3-83cb-d5414d76e1d2
  Args:
    target: Frederick_Francis_II_of_Mecklenburg-Schwerin
    source: Adolf_Friedrich_of_Mecklenburg-Schwerin
    relation: :hasFather
  AddTriple (53d7c0cc-d7fa-4924-9995-0dcf913a01b5)
 Call ID: 53d7c0cc-d7fa-4924-9995-0dcf913a01b5
  Args:
    target: Marie_of_Schwarzburg-Rudolstadt
    source: Adolf_Friedrich_of_Mecklenburg-Schwerin
    relation: :hasMother
  AssignClass (d4c428aa-5863-4b5c-b5c0-7755967c460c)
 Call ID: d4c428aa-5863-4b5c-b5c0-7755967c460c
  Args:
    type: :Woman
    source: Viktoria_Feodora_of_Reuss-Schleiz
  AssignClass (eeddbe10-6edf-4545-9aab-63f403af2581)
 Call ID: eeddbe10-6edf-4545-9aab-63f403af2581
  Args:
    type: :Person
    source: Viktoria_Feodora_of_Reuss-Schleiz
  AddLiteral (997db303-e3a9-423a-9ec9-0a8accd41a93)
 Call ID: 997db303-e3a9-423a-9ec9-0a8accd41a93
  Args:
    relation: :hasMarriageYear
    literal_value: 1917
    source: Adolf_Friedrich_of_Mecklenburg-Schwerin
    literal_type: xsd:integer
  AssignClass (5c8fc227-a258-4dce-809a-5aaf9d0c3821)
 Call ID: 5c8fc227-a258-4dce-809a-5aaf9d0c3821
  Args:
    type: :Woman
    source: Elisabeth_of_Stolberg-Rossla
  AssignClass (cb092f83-d107-4f90-97b6-728a6757b91a)
 Call ID: cb092f83-d107-4f90-97b6-728a6757b91a
  Args:
    type: :Person
    source: Elisabeth_of_Stolberg-Rossla
  AddLiteral (eb3d5c5c-8680-47f6-b535-3e587cb93883)
 Call ID: eb3d5c5c-8680-47f6-b535-3e587cb93883
  Args:
    source: Adolf_Friedrich_of_Mecklenburg-Schwerin
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1924
  AssignClass (032c2b97-236d-4e3d-91d8-bc6791335c1c)
 Call ID: 032c2b97-236d-4e3d-91d8-bc6791335c1c
  Args:
    type: :Man
    source: John_Albert_of_Mecklenburg-Schwerin
  AssignClass (cc1dc3e9-7651-47a3-9773-e7220a719aab)
 Call ID: cc1dc3e9-7651-47a3-9773-e7220a719aab
  Args:
    type: :Person
    source: John_Albert_of_Mecklenburg-Schwerin
  AddTriple (bbc2f175-7cc1-4090-a9ae-698b9e958995)
 Call ID: bbc2f175-7cc1-4090-a9ae-698b9e958995
  Args:
    relation: :isBrotherOf
    target: John_Albert_of_Mecklenburg-Schwerin
    source: Adolf_Friedrich_of_Mecklenburg-Schwerin
  Finish (c1897f42-c40c-4bdf-9607-f047ce60ed47)
 Call ID: c1897f42-c40c-4bdf-9607-f047ce60ed47
  Args: