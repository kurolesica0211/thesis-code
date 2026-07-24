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
  AssignClass (546a9666-084b-4bfe-a84e-c935ce965d1e)
 Call ID: 546a9666-084b-4bfe-a84e-c935ce965d1e
  Args:
    type: :Man
    source: :Karl_von_Habsburg
  AssignClass (503b8269-2f51-4239-b201-beddc1d7baf1)
 Call ID: 503b8269-2f51-4239-b201-beddc1d7baf1
  Args:
    type: :Person
    source: :Karl_von_Habsburg
  AddLiteral (f968b48f-2f67-486b-af6f-cdd5a8288106)
 Call ID: f968b48f-2f67-486b-af6f-cdd5a8288106
  Args:
    relation: :alsoKnownAs
    source: :Karl_von_Habsburg
    literal_value: Karl Thomas Robert Maria Franziskus Georg Bahnam
    literal_type: xsd:string
  AddLiteral (0d782c06-97d5-41ca-ac14-8b47af2958e4)
 Call ID: 0d782c06-97d5-41ca-ac14-8b47af2958e4
  Args:
    source: :Karl_von_Habsburg
    relation: :alsoKnownAs
    literal_value: Karl Habsburg-Lothringen
    literal_type: xsd:string
  AddLiteral (08d19893-aed4-400c-90c8-d9e2ff778d62)
 Call ID: 08d19893-aed4-400c-90c8-d9e2ff778d62
  Args:
    literal_type: xsd:integer
    literal_value: 1961
    source: :Karl_von_Habsburg
    relation: :hasBirthYear
  AssignClass (46a9474b-0ba9-4e67-b139-98b7dcac159c)
 Call ID: 46a9474b-0ba9-4e67-b139-98b7dcac159c
  Args:
    type: :Man
    source: :Otto_von_Habsburg
  AssignClass (4220e2d3-e023-438d-ac45-cdad9c685335)
 Call ID: 4220e2d3-e023-438d-ac45-cdad9c685335
  Args:
    type: :Person
    source: :Otto_von_Habsburg
  AssignClass (16728356-b081-43ba-9353-cfdf59ad7ede)
 Call ID: 16728356-b081-43ba-9353-cfdf59ad7ede
  Args:
    type: :Woman
    source: :Regina_von_Sachsen_Meiningen
  AssignClass (7fc08600-d92a-4f78-bb18-68c74a929069)
 Call ID: 7fc08600-d92a-4f78-bb18-68c74a929069
  Args:
    type: :Person
    source: :Regina_von_Sachsen_Meiningen
  AddTriple (2f5dbdd4-ab82-4c47-9695-eda1683072a6)
 Call ID: 2f5dbdd4-ab82-4c47-9695-eda1683072a6
  Args:
    source: :Karl_von_Habsburg
    target: :Otto_von_Habsburg
    relation: :hasFather
  AddTriple (fbb164d6-73c1-4113-8ea9-3ba4e49917b6)
 Call ID: fbb164d6-73c1-4113-8ea9-3ba4e49917b6
  Args:
    relation: :hasMother
    target: :Regina_von_Sachsen_Meiningen
    source: :Karl_von_Habsburg
  AssignClass (ebc0e970-6b53-455e-abec-22d8c244c153)
 Call ID: ebc0e970-6b53-455e-abec-22d8c244c153
  Args:
    type: :Man
    source: :Charles_I
  AssignClass (126a0e3c-4411-4204-a920-a39b010a555f)
 Call ID: 126a0e3c-4411-4204-a920-a39b010a555f
  Args:
    type: :Person
    source: :Charles_I
  AddTriple (5cfc9649-5a2a-4ba0-83d6-6a1db20b5d63)
 Call ID: 5cfc9649-5a2a-4ba0-83d6-6a1db20b5d63
  Args:
    target: :Charles_I
    source: :Karl_von_Habsburg
    relation: :hasAncestor
  AssignClass (fc631ba2-ede0-4f2f-a2fc-a063c942188a)
 Call ID: fc631ba2-ede0-4f2f-a2fc-a063c942188a
  Args:
    type: :Woman
    source: :Francesca_Thyssen_Bornemisza
  AssignClass (2535bc99-e8fd-45cb-afe8-56b2f936169e)
 Call ID: 2535bc99-e8fd-45cb-afe8-56b2f936169e
  Args:
    type: :Person
    source: :Francesca_Thyssen_Bornemisza
  AddLiteral (1d12aa2f-e710-484a-b00f-068c04e8d8ea)
 Call ID: 1d12aa2f-e710-484a-b00f-068c04e8d8ea
  Args:
    source: :Francesca_Thyssen_Bornemisza
    relation: :knownAs
    literal_value: Francesca Thyssen-Bornemisza
    literal_type: xsd:string
  AddLiteral (a92d122b-f729-4d11-9e98-fbe914036df8)
 Call ID: a92d122b-f729-4d11-9e98-fbe914036df8
  Args:
    source: :Karl_von_Habsburg
    relation: :hasMarriageYear
    literal_type: xsd:integer
    literal_value: 1993
  AssignClass (7084507e-35e9-49fc-abb6-68554a6a46a1)
 Call ID: 7084507e-35e9-49fc-abb6-68554a6a46a1
  Args:
    type: :Man
    source: :Hans_Heinrich_Thyssen_Bornemisza
  AssignClass (7877dea4-807b-4bda-914b-e89987aba9c4)
 Call ID: 7877dea4-807b-4bda-914b-e89987aba9c4
  Args:
    type: :Person
    source: :Hans_Heinrich_Thyssen_Bornemisza
  AssignClass (8fb51b4f-11d4-4189-8b8c-91cefd798e86)
 Call ID: 8fb51b4f-11d4-4189-8b8c-91cefd798e86
  Args:
    type: :Woman
    source: :Fiona_Frances_Elaine_Campbell_Walter
  AssignClass (027a0e95-6a6d-4176-b858-c37e9f583aa8)
 Call ID: 027a0e95-6a6d-4176-b858-c37e9f583aa8
  Args:
    type: :Person
    source: :Fiona_Frances_Elaine_Campbell_Walter
  AddTriple (0b17b6e9-f58c-4a34-bb2e-2d917b18651f)
 Call ID: 0b17b6e9-f58c-4a34-bb2e-2d917b18651f
  Args:
    source: :Francesca_Thyssen_Bornemisza
    target: :Hans_Heinrich_Thyssen_Bornemisza
    relation: :hasFather
  AddTriple (e96eb048-3cc4-4ab9-b0e9-28412e6560f0)
 Call ID: e96eb048-3cc4-4ab9-b0e9-28412e6560f0
  Args:
    relation: :hasMother
    source: :Francesca_Thyssen_Bornemisza
    target: :Fiona_Frances_Elaine_Campbell_Walter
  AssignClass (925d9164-85b1-4076-9c9a-fd23b41cd5d5)
 Call ID: 925d9164-85b1-4076-9c9a-fd23b41cd5d5
  Args:
    type: :Woman
    source: :Christian_Nicolau_de_Almeida_Reid
  AssignClass (d8c81919-79f9-419a-b707-0ef8a859bbc9)
 Call ID: d8c81919-79f9-419a-b707-0ef8a859bbc9
  Args:
    type: :Person
    source: :Christian_Nicolau_de_Almeida_Reid
  Finish (7b8dd526-27d5-4bfd-9e2b-7db52da2b8a1)
 Call ID: 7b8dd526-27d5-4bfd-9e2b-7db52da2b8a1
  Args: