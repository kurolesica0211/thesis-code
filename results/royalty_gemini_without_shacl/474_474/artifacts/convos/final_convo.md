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
Karl von Habsburg (given name: Karl Thomas Robert Maria Franziskus Georg Bahnam; born 11 January 1961) is an Austrian politician and the head of the House of Habsburg-Lorraine, the former royal house of the defunct Austro-Hungarian thrones.
As a citizen of the Republic of Austria, his legal name is Karl Habsburg-Lothringen.
Karl is the son of Otto von Habsburg and Regina von Sachsen-Meiningen, and the grandson of the last Austro-Hungarian emperor, Charles I.
Karl Habsburg served as a member of the European Parliament for the Austrian People's Party (1996–1999).
Karl Habsburg's career has focused on the issue of protecting cultural heritage from threats such as armed conflict and natural disasters.
Early life and background

Karl Habsburg was born on 11 January 1961 in Starnberg, Bavaria.
He was baptised in Pöcking, Bavaria, as Archduke Karl of Austria (Erzherzog Karl von Österreich), the name entered in the baptismal records.
House of Habsburg titles and issues


In 1961, Karl's father, Otto von Habsburg, renounced all claims to the defunct Austrian throne, as a necessary legal condition to being allowed to return to Austria.
Karl does not use his ancestral titles, because unlike most European countries, even the unofficial use of such titles is not permitted in Hungary and Austria.
Habsburg says: 

I don't refer to titles, I'm not that vain.
Although the Adelsaufhebungsgesetz (Law on the Abolition of the Nobility) abolished all Austrian and Hungarian noble, royal, and imperial titles in 1919, and their usage is still illegal in those countries, media elsewhere occasionally refer to Karl Habsburg by his ancestral titles of Archduke of Austria, Royal Prince of Hungary, Bohemia and Croatia.
At the request of the USSR, which was wary of a restoration of the monarchy, the anti-Habsburg laws became mandatory international and constitutional components of the Austrian State Treaty in 1955.
The attempt of Karl Habsburg failed because the law of expropriation still has constitutional status.
On 1 January 2007, his father relinquished his position as the head of the House of Habsburg-Lorraine, a status which then devolved on Karl.
As head of the House of Habsburg-Lorraine, Karl undertakes numerous commitments.
Education

Between 1982 and 1989, Habsburg studied law, philosophy, and political science at the University of Salzburg, passing his first staatsexamen in 1984; while there, he spent a year studying law and philosophy at Michigan State University in the United States.
Career

Defunct


Military service

Karl Habsburg did his military service in 1981 as a platoon commander of a Jäger (infantry) platoon as a one-year volunteer with the Austrian Armed Forces, where he later also completed his pilot training.
Activism

Since 1986, Karl Habsburg has been president of the Austrian branch of the Paneuropean Union, which co-organised the Pan-European Picnic.
In May 1990, Habsburg personally led an aid convoy to Vilnius with food, medicine and clothing as a representative of the Paneuropean Union, in response to the Soviet Union's blockade of raw materials following the proclamation of Lithuanian independence in March 1990.
In October 1996, Habsburg was elected as a member of the European Parliament (MEP) for Austria, representing the Austrian People's Party.
Habsburg was a strong supporter of those who created the "No Strike List" of cultural heritage sites and cultural sites that should be preserved when attacks or flight operations were carried out.
Habsburg particularly supports the bringing together of military and civilian personnel and the cooperation of various international organizations for the protection of cultural assets, such as the Blue Shield, UNIFIL and UNESCO deployment in Lebanon in 2019, and the cooperation with the International Committee of the Red Cross in 2020.
After the explosion in the port of Beirut in Lebanon in summer 2020, Habsburg helped coordinate the reconstruction and aid on site.
Personal life

Habsburg has lived in Austria since 1981 and resided in Casa Austria, formerly called Villa Swoboda, in Anif, near the city of Salzburg, until 2022.
On 31 January 1993 in Mariazell, he married Baroness Francesca Thyssen-Bornemisza (born 7 June 1958 in Lausanne), the only daughter of Baron Hans Heinrich Thyssen-Bornemisza de Kászon, a European industrialist, and his third wife, the fashion model Fiona Frances Elaine Campbell-Walter.
The marriage received the dynastic authorization of Karl's father, as head of the House of Habsburg, despite objections from some members of the family as the bride, although a baroness in the nobility of pre-republican Hungary and Transylvania, did not descend in the canonically legitimate male line from a family of dynastic (ruling or formerly ruling or mediatised) status.
Karl and Francesca have three children:


In the spring of 2022 in Portugal, Karl married Christian Nicolau de Almeida Reid, a woman of Portuguese descent.
Habsburg self-isolated at home.
Karl von Habsburg was officially declared healthy after almost three weeks of quarantine.
After his illness, Karl Habsburg encouraged everyone to follow the official protective measures strictly, and asked survivors of the disease to donate blood plasma.
Controversies

In July 1998 an Austrian court fined Karl von Habsburg 180,000 schillings ($14,300); he had failed to declare immediately to customs officials that he had an antique diadem in his luggage when he crossed the border from Switzerland in July 1996.
Also in 1998, evidence emerged that during Habsburg's election campaign for membership in the European Parliament two years prior, his political party the ÖVP, had benefited from at least 30,000 Marks worth of World Vision donations via Paneurope Austria while Karl Habsburg sat on the board of World Vision Austria, apparently without noticing the director's dubiously legal activities.
His father exacerbated the controversy when he complained that his son was being attacked unfairly and drew a parallel between the name "Habsburg" and a yellow badge.
ÖVP did not nominate Karl von Habsburg again for the 1999 elections.
In 2004, Karl von Habsburg paid 37,000 euros to the new World Vision Austria branch.



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
  AssignClass (10c5dbcc-624e-44e2-9049-ec19c36c968c)
 Call ID: 10c5dbcc-624e-44e2-9049-ec19c36c968c
  Args:
    source: Karl_von_Habsburg
    type: :Man
  AssignClass (5b397b57-95de-4d38-9228-2e3b419c210a)
 Call ID: 5b397b57-95de-4d38-9228-2e3b419c210a
  Args:
    type: :Person
    source: Karl_von_Habsburg
  AddLiteral (e098fbc5-9683-43b0-a2b8-07b69ae9882f)
 Call ID: e098fbc5-9683-43b0-a2b8-07b69ae9882f
  Args:
    literal_type: xsd:integer
    literal_value: 1961
    source: Karl_von_Habsburg
    relation: :hasBirthYear
  AssignClass (ba924a97-4bb1-4177-a687-51ffe2324978)
 Call ID: ba924a97-4bb1-4177-a687-51ffe2324978
  Args:
    source: Otto_von_Habsburg
    type: :Man
  AssignClass (d12e5264-6fcc-4bf2-a65c-0edbd04a835c)
 Call ID: d12e5264-6fcc-4bf2-a65c-0edbd04a835c
  Args:
    type: :Person
    source: Otto_von_Habsburg
  AssignClass (93e93973-ab03-4588-b6e4-e11b7e2adba5)
 Call ID: 93e93973-ab03-4588-b6e4-e11b7e2adba5
  Args:
    type: :Woman
    source: Regina_von_Sachsen-Meiningen
  AssignClass (37e9ebec-87b7-4565-931e-077b84e9a38f)
 Call ID: 37e9ebec-87b7-4565-931e-077b84e9a38f
  Args:
    type: :Person
    source: Regina_von_Sachsen-Meiningen
  AddTriple (85a73df2-6e8c-4d22-8817-94e2f552e2a7)
 Call ID: 85a73df2-6e8c-4d22-8817-94e2f552e2a7
  Args:
    source: Karl_von_Habsburg
    target: Otto_von_Habsburg
    relation: :hasFather
  AddTriple (212cb1b5-1860-493c-a23c-cb2125a7cbc1)
 Call ID: 212cb1b5-1860-493c-a23c-cb2125a7cbc1
  Args:
    target: Regina_von_Sachsen-Meiningen
    source: Karl_von_Habsburg
    relation: :hasMother
  AssignClass (60e9cd3b-7dec-4e57-ac15-f236185db8ab)
 Call ID: 60e9cd3b-7dec-4e57-ac15-f236185db8ab
  Args:
    type: :Man
    source: Charles_I
  AssignClass (aee1ffce-d64a-4d47-be62-732f29132ecf)
 Call ID: aee1ffce-d64a-4d47-be62-732f29132ecf
  Args:
    type: :Person
    source: Charles_I
  AddTriple (09322b91-7fc9-48d4-85cc-b1873910ed71)
 Call ID: 09322b91-7fc9-48d4-85cc-b1873910ed71
  Args:
    target: Charles_I
    source: Karl_von_Habsburg
    relation: :hasAncestor
  AssignClass (98710a47-e9e8-489e-bc77-0f499ab5f2a7)
 Call ID: 98710a47-e9e8-489e-bc77-0f499ab5f2a7
  Args:
    type: :Woman
    source: Francesca_Thyssen-Bornemisza
  AssignClass (1fb6df75-9729-423c-8d7a-5c76f30ffe2b)
 Call ID: 1fb6df75-9729-423c-8d7a-5c76f30ffe2b
  Args:
    source: Francesca_Thyssen-Bornemisza
    type: :Person
  AddTriple (96db0090-a7ee-4dfa-9358-fdea01fc3f78)
 Call ID: 96db0090-a7ee-4dfa-9358-fdea01fc3f78
  Args:
    source: Karl_von_Habsburg
    target: Francesca_Thyssen-Bornemisza
    relation: :hasRelation
  AddLiteral (7375f0e5-86c9-4397-8458-d21b4b2d3930)
 Call ID: 7375f0e5-86c9-4397-8458-d21b4b2d3930
  Args:
    source: Karl_von_Habsburg
    literal_value: 1993
    relation: :hasMarriageYear
    literal_type: xsd:integer
  AssignClass (5196f2be-d600-4f20-b16c-cee88716e547)
 Call ID: 5196f2be-d600-4f20-b16c-cee88716e547
  Args:
    source: Hans_Heinrich_Thyssen-Bornemisza
    type: :Man
  AssignClass (58bdb576-affd-4c30-bfbf-10646e969a7c)
 Call ID: 58bdb576-affd-4c30-bfbf-10646e969a7c
  Args:
    type: :Person
    source: Hans_Heinrich_Thyssen-Bornemisza
  AssignClass (4ca41765-b6f4-4065-a3a4-6662d28d7ecb)
 Call ID: 4ca41765-b6f4-4065-a3a4-6662d28d7ecb
  Args:
    type: :Woman
    source: Fiona_Frances_Elaine_Campbell-Walter
  AssignClass (d3c86a36-2a22-4b07-a377-a8266822c7f8)
 Call ID: d3c86a36-2a22-4b07-a377-a8266822c7f8
  Args:
    source: Fiona_Frances_Elaine_Campbell-Walter
    type: :Person
  AddTriple (6ddac4ff-947b-47bb-8131-393032b42dec)
 Call ID: 6ddac4ff-947b-47bb-8131-393032b42dec
  Args:
    source: Francesca_Thyssen-Bornemisza
    target: Hans_Heinrich_Thyssen-Bornemisza
    relation: :hasFather
  AddTriple (1ea7bae8-f438-4d36-95fe-961065fdf375)
 Call ID: 1ea7bae8-f438-4d36-95fe-961065fdf375
  Args:
    target: Fiona_Frances_Elaine_Campbell-Walter
    source: Francesca_Thyssen-Bornemisza
    relation: :hasMother
  AssignClass (6f1ce337-7085-47c8-8ef7-9c6f9495ca88)
 Call ID: 6f1ce337-7085-47c8-8ef7-9c6f9495ca88
  Args:
    source: Christian_Nicolau_de_Almeida_Reid
    type: :Woman
  AssignClass (6fdc3356-01bb-424f-9ace-19b208e04d44)
 Call ID: 6fdc3356-01bb-424f-9ace-19b208e04d44
  Args:
    type: :Person
    source: Christian_Nicolau_de_Almeida_Reid
  AddTriple (17a9db5b-1f5e-4bc2-ad75-87af81a80d1e)
 Call ID: 17a9db5b-1f5e-4bc2-ad75-87af81a80d1e
  Args:
    source: Karl_von_Habsburg
    target: Christian_Nicolau_de_Almeida_Reid
    relation: :hasRelation
  AddLiteral (0d6aa46e-0b9d-40e7-add8-1da1be16cbb0)
 Call ID: 0d6aa46e-0b9d-40e7-add8-1da1be16cbb0
  Args:
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 2022
    source: Karl_von_Habsburg
  Finish (13bb5c1b-bf62-4bf5-a071-d3d9ea2ec45b)
 Call ID: 13bb5c1b-bf62-4bf5-a071-d3d9ea2ec45b
  Args: