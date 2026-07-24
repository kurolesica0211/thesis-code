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
Descendants of Prince Felix and also members of the Grand Ducal Family of Luxembourg:


Princess Joan


Descendants of Prince René:


Princess Maria Pia


Princess Marina


Descendants of Prince Louis:


Prince RémyPrincess Elisabeth


Princess Chantal
Prince JeanPrincess Virginia


Princess Beatrix*


Princess Margriet*Pieter van Vollenhoven*


Prince Carlos, Duke of Parma and Piacenza (Carlos Xavier Bernardo Sixto Marie; born 27 January 1970) is the current Head of the House of Bourbon-Parma, which ruled the Duchy of Parma and Piacenza from 1748 to 1802 and from 1847 to 1859.
The eldest son of Carlos Hugo, Duke of Parma and Princess Irene of the Netherlands, Carlos is also a member of the Dutch royal family and the Dutch nobility with the style of "His Royal Highness" and the title of Prince Carlos de Bourbon de Parme.
Additionally, he is the Carlist pretender to the Spanish throne with the title Duke of Madrid.
In the French nobility, he bears the title "Prince de Borbon", and is the grand master of the Parmesan Sacred Military Constantinian Order of Saint George, the Order of Saint Louis for Civil Merit, the Order of Prohibited Legitimacy and the Order of St. George for Military Merit.
Early life

Prince Carlos Xavier Bernardo Sixto Marie of Bourbon-Parma was born in Nijmegen, The Netherlands on 27 January 1970 as the elder child and son of Carlos Hugo, Duke of Parma, and his wife Princess Irene of the Netherlands.
He has two younger sisters, Princess Margarita and Princess Carolina, and a younger brother, Prince Jaime.
At the time of his birth, his parents, Carlist Pretender to the Spanish throne, were expelled from Spain by the Franco regime since 20 December 1968, as Franco already did with his grandfather Prince Xavier of Bourbon-Parma and some members of his family on 25 November 1937.
Carlos spent his youth in several countries including the Netherlands, Spain, France, England, and the United States.
Together with his mother and his siblings, he then moved to Soestdijk Palace (Baarn) in the Netherlands.
He lived at the palace for a number of years with his maternal grandparents, Queen Juliana of the Netherlands and Prince Bernhard.
Education and career

Prince Carlos studied political science at Wesleyan University in Connecticut and demography and philosophy at Cambridge University in England; in 1995, he obtained a Postgraduate Degree (MPhil) in Demography at the Cambridge University.
After completing his studies, Carlos worked for the company ABN AMRO in Amsterdam, where he was involved with preparations for the introduction of the euro.
He has chaired the Foundation for Cooperation for the Economic Development of Latin America, was a member for eight years of the Council of CSR Netherlands, which ensures corporate social responsibility.
Duties and appearances

Dutch Royal House

Carlos is sometimes present at representative occasions concerning the Royal House of the Netherlands.
In 2003, he was involved, together with his aunt, Queen Beatrix, in the inauguration of the "Prince Claus Leerstoel", a professorship named after the Queen's husband, Prince Claus.
For example, he was one of the organizers of the wedding celebration of Prince Constantijn and Princess Laurentien.
In April 2013, Prince Carlos attended the inauguration of his cousin King Willem-Alexander and his wife Queen Maxima in Amsterdam.
In August 2019 he and his wife attended the funeral of his aunt Princess Christina of the Netherlands, sister of former Queen Beatrix, near Noordeinde Palace, The Hague.
His rights as the Carlist pretender

After the death of his father Carlos Hugo in 2010, Prince Carlos Xavier succeeded him as Duke of Madrid and Carlist Pretender to the Spanish throne.
He started to use the Carlist title of "Rey Don Carlos Javier I" (King Don Carlos Xavier I).
However, Carlos Xavier, in an interview with the newspaper La Vanguardia, said:


I don't set out dynastic lawsuits.
— Barcelona, October 11th, 2010

Duke of Parma

Prince Carlos became Duke of Parma and Piacenza and Head of the House of Bourbon-Parma after the death of his father on 18 August 2010, aged 80.
In 2016, at the baptism of Prince Carlos Enrique, Prince Carlos conferred on his son the title of "Principe di Piacenza" (Prince of Piacenza), which is the traditional title assigned to the Crown Prince of the House of Bourbon-Parma, the continuer of the dynasty, and future Duke of Parma and Piacenza.
In September 2017, the Duke of Parma named his daughter Princess Luisa as "Marchesa di Castell'Arquato" (Marquise of Castell'Arquato), and her younger sister Princess Cecilia was named as "Contessa di Berceto" (Countess of Berceto).
Prince Carlos has visited and regularly visits the lands of the former Duchy of Parma and Piacenza.
In September 2015, he was in Parma to grant the "Prince's Medal to Meritorious Men in silver" to the firefighters who distinguished themselves during the 2015 flood that struck the area.
At the end of September 2017, he presided over the General Chapter of the Knights of the House of Bourbon-Parma in Parma to confer the Ducal orders to those people who have achieved personal merits towards the Royal House; then he visited Palazzo della Pilotta.
In September 2018, he visited Parma to confer some honors of the Royal House and to visit the Church of Santa Maria della Steccata, together with the Royal Family.
Also, he was present at the inauguration of the opera season by attending a representation of the opera "Macbeth" at the Teatro Regio in Parma and made a visit to the Military Academy of Modena, received by the Commander.
As Duke of Parma, Prince Carlos is committed to preserving the memory of the lands and members and relatives of the dynasty: in July 2011 he was in Vienna to attend the funeral of Archduke Otto, the last Crown Prince of Austria-Hungary (son of Princess Zita of Bourbon-Parma, sister to Carlos' grandfather Prince Xavier) at the St. Stephen's Cathedral.
In August 2016, Prince Carlos was in Romania to attend the funeral of Queen Anne (née Princess of Bourbon-Parma as a daughter of Prince René, brother of Carlos' grandfather) in Curtea de Argeș.
At the funeral, Carlos represented also the Dutch Royal Family who was unable to attend.
In June 2018 he traveled to Prague to remember his ancestor Maria Amalia, Duchess of Parma, and to take part in the presentation of the book "Maria Amalia Duchess of Parma and Piacenza (1746–1804)" dedicated to the life of his ancestor, and later visited the Cathedral of San Vito in Prague to lay flowers on the tomb of Duchess Maria Amalia.
Personal life

Relationship with Brigitte Klynstra and son

Prince Carlos had a relationship with Brigitte Klynstra (born 10 January 1959), the stepdaughter of Count Adolph Roderik of Rechteren-Limpurg.
In December 2015, the then 18-year-old Carlos Klynstra started the legal procedure to attempt to change his surname to that of his biological father which would also allow him to use the title of "Prince".
The Duke of Parma opposed this on the basis that it was in contravention of the traditions of the House of Bourbon-Parma.
According to the judgement, Carlos Hugo will be entitled to be known as "Zijne Koninklijke Hoogheid Carlos Hugo Roderik Sybren prins de Bourbon de Parme" (His Royal Highness Prince Carlos Hugo Roderik Sybren of Bourbon-Parma); this will come only into effect once the Dutch king has signed the royal decree.
According to the press release of the Council of State of 28 February 2018, the name change does not mean that Klynstra is now also a member of the Royal House of  Bourbon-Parma.
Marriage to Annemarie Gualthérie van Weezel

On 7 October 2009, it was announced through his mother's private secretary that Prince Carlos would marry Annemarie Cecilia
Prince Carlos Hugo died shortly afterwards.
Her father was a member of the House of Representatives of the Netherlands for the Christian Democratic party, the Dutch ambassador to the Council of Europe in Strasbourg, and the ambassador to Luxembourg.
In Brussels, she met Prince Carlos for the first time.
On 2 August 2010, it was revealed that the health of his father, the Duke of Parma, was quickly deteriorating due to cancer.
As a consequence, the church wedding of the prince Carlos and his fiancée was delayed.
In a final announcement about his condition, the Duke confirmed Carlos as the next Head of the House of Bourbon-Parma.
Just before his death the old Duke of Parma named Annemarie as "Condesa de Molina" (Countess of Molina).
Prince Carlos's father died on 18 August 2010 in Barcelona, Spain, at the age of 80; Carlos subsequently became the next head of the House of Bourbon-Parma.
The new Duke of Parma and Annemarie were married on 20 November 2010 in La Cambre Abbey in Bruxelles.
The wedding was attended by Máxima, Princess of Orange, Willem-Alexander, Prince of Orange, Queen Beatrix of the Netherlands, Prince Jean of Luxembourg, Princess Astrid of Belgium, Prince Lorenz of Belgium and Duarte Pio, Duke of Braganza.
Together, they have two daughters and a son:


Titles, styles and honours

Titles and styles

Honours

Dynastic

As Head of the House of Bourbon-Parma, Carlos is Grand Master of four dynastic orders:


National

International

Ancestry

Notes

References

External links

2 gave up the title "Prince of the Netherlands, but still held the title "Prince of Orange-Nassau"
3 title granted by Royal Decree to descendants of Princess Irene



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
  AssignClass (ac02aafb-38c3-461f-98ce-43a0a1738f7e)
 Call ID: ac02aafb-38c3-461f-98ce-43a0a1738f7e
  Args:
    type: :Man
    source: :PrinceCarlos
  AssignClass (7b3822f6-797d-451f-86d5-e1a05cc54c52)
 Call ID: 7b3822f6-797d-451f-86d5-e1a05cc54c52
  Args:
    type: :Person
    source: :PrinceCarlos
  AssignClass (9e34dcf2-9ca8-489f-a92d-4fbc06964c59)
 Call ID: 9e34dcf2-9ca8-489f-a92d-4fbc06964c59
  Args:
    type: :Man
    source: :CarlosHugo
  AssignClass (0998d233-37ff-4e76-a483-4466d352849e)
 Call ID: 0998d233-37ff-4e76-a483-4466d352849e
  Args:
    type: :Person
    source: :CarlosHugo
  AssignClass (55569361-f04e-4c8b-9d8e-5d2d5607b439)
 Call ID: 55569361-f04e-4c8b-9d8e-5d2d5607b439
  Args:
    type: :Woman
    source: :PrincessIrene
  AssignClass (78bf2e4e-5dfe-4f87-8006-d4f564455b90)
 Call ID: 78bf2e4e-5dfe-4f87-8006-d4f564455b90
  Args:
    type: :Person
    source: :PrincessIrene
  AddLiteral (946a353a-0b71-4cc6-92a7-08a328dcb46f)
 Call ID: 946a353a-0b71-4cc6-92a7-08a328dcb46f
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: :PrinceCarlos
    literal_value: 1970
  AddTriple (267d487a-823e-4a2a-afd7-e4e75d155ffe)
 Call ID: 267d487a-823e-4a2a-afd7-e4e75d155ffe
  Args:
    target: :CarlosHugo
    source: :PrinceCarlos
    relation: :hasFather
  AddTriple (c263b6c2-313f-4ce5-9bdd-f1d339964f49)
 Call ID: c263b6c2-313f-4ce5-9bdd-f1d339964f49
  Args:
    source: :PrinceCarlos
    target: :PrincessIrene
    relation: :hasMother
  AssignClass (fe69af8e-7c57-4bbb-995f-04c090672c1a)
 Call ID: fe69af8e-7c57-4bbb-995f-04c090672c1a
  Args:
    type: :Woman
    source: :PrincessMargarita
  AssignClass (f9763ab9-6a4e-4a2c-a132-db939b8bfe11)
 Call ID: f9763ab9-6a4e-4a2c-a132-db939b8bfe11
  Args:
    type: :Person
    source: :PrincessMargarita
  AssignClass (7a73b44a-c8e6-45d2-9764-f259bbd0ead7)
 Call ID: 7a73b44a-c8e6-45d2-9764-f259bbd0ead7
  Args:
    type: :Woman
    source: :PrincessCarolina
  AssignClass (316df5c8-760c-4382-9d76-182530700f4c)
 Call ID: 316df5c8-760c-4382-9d76-182530700f4c
  Args:
    type: :Person
    source: :PrincessCarolina
  AssignClass (f36e2d6d-f802-44b1-9fa3-6335b504f41b)
 Call ID: f36e2d6d-f802-44b1-9fa3-6335b504f41b
  Args:
    type: :Man
    source: :PrinceJaime
  AssignClass (5990a602-3a0e-408b-b103-19d5a7772aa2)
 Call ID: 5990a602-3a0e-408b-b103-19d5a7772aa2
  Args:
    type: :Person
    source: :PrinceJaime
  AddTriple (8814fc4c-cb7f-43dc-a09b-c270f6e7f853)
 Call ID: 8814fc4c-cb7f-43dc-a09b-c270f6e7f853
  Args:
    target: :PrincessMargarita
    source: :PrinceCarlos
    relation: :hasSister
  AddTriple (3f69ac89-e6b3-4a27-b81f-2e2fc5da78c6)
 Call ID: 3f69ac89-e6b3-4a27-b81f-2e2fc5da78c6
  Args:
    target: :PrincessCarolina
    source: :PrinceCarlos
    relation: :hasSister
  AddTriple (3573e753-db49-4a21-8e6a-10e0b1239faf)
 Call ID: 3573e753-db49-4a21-8e6a-10e0b1239faf
  Args:
    relation: :hasBrother
    target: :PrinceJaime
    source: :PrinceCarlos
  AddTriple (6493faec-ffdd-47d8-8dc1-33d24f4a5036)
 Call ID: 6493faec-ffdd-47d8-8dc1-33d24f4a5036
  Args:
    relation: :hasFather
    source: :PrincessMargarita
    target: :CarlosHugo
  AddTriple (3748f802-a110-4bca-aaa6-5c08d40074c8)
 Call ID: 3748f802-a110-4bca-aaa6-5c08d40074c8
  Args:
    relation: :hasMother
    target: :PrincessIrene
    source: :PrincessMargarita
  AddTriple (00fc352f-252b-48e9-acfb-8c4b68df8602)
 Call ID: 00fc352f-252b-48e9-acfb-8c4b68df8602
  Args:
    relation: :hasFather
    source: :PrincessCarolina
    target: :CarlosHugo
  AddTriple (05c1ff13-b148-484e-8a88-dc2163fea8d6)
 Call ID: 05c1ff13-b148-484e-8a88-dc2163fea8d6
  Args:
    relation: :hasMother
    source: :PrincessCarolina
    target: :PrincessIrene
  AddTriple (1fbf3259-6531-4229-823b-9269ebfaca79)
 Call ID: 1fbf3259-6531-4229-823b-9269ebfaca79
  Args:
    relation: :hasFather
    target: :CarlosHugo
    source: :PrinceJaime
  AddTriple (81a6ade4-45ff-4e96-ba08-8900c4353a59)
 Call ID: 81a6ade4-45ff-4e96-ba08-8900c4353a59
  Args:
    source: :PrinceJaime
    target: :PrincessIrene
    relation: :hasMother
  AssignClass (44fdde28-f2c7-4564-b6e8-7baf99d10012)
 Call ID: 44fdde28-f2c7-4564-b6e8-7baf99d10012
  Args:
    type: :Man
    source: :PrinceXavier
  AssignClass (4ae8fc68-00ed-414f-8dde-b144cbd5c0b8)
 Call ID: 4ae8fc68-00ed-414f-8dde-b144cbd5c0b8
  Args:
    type: :Person
    source: :PrinceXavier
  AddTriple (f2eb314a-34d2-4a7f-9c69-58d153e219a8)
 Call ID: f2eb314a-34d2-4a7f-9c69-58d153e219a8
  Args:
    relation: :hasFather
    target: :PrinceXavier
    source: :CarlosHugo
  AssignClass (49ab27eb-0fbc-484e-a74e-1b4d2617ebdd)
 Call ID: 49ab27eb-0fbc-484e-a74e-1b4d2617ebdd
  Args:
    type: :Man
    source: :PrinceCarlosEnrique
  AssignClass (58f3949c-c849-44eb-8f4d-d80a65e1a35f)
 Call ID: 58f3949c-c849-44eb-8f4d-d80a65e1a35f
  Args:
    type: :Person
    source: :PrinceCarlosEnrique
  AddTriple (6dc693ab-afda-459d-836d-9fe5e758f66e)
 Call ID: 6dc693ab-afda-459d-836d-9fe5e758f66e
  Args:
    relation: :hasFather
    target: :PrinceCarlos
    source: :PrinceCarlosEnrique
  AssignClass (f007f2ff-2f27-45c3-b692-1596dcb40d32)
 Call ID: f007f2ff-2f27-45c3-b692-1596dcb40d32
  Args:
    type: :Woman
    source: :PrincessLuisa
  AssignClass (4864fa7a-a325-47aa-8103-425dadd6c31f)
 Call ID: 4864fa7a-a325-47aa-8103-425dadd6c31f
  Args:
    type: :Person
    source: :PrincessLuisa
  AssignClass (50150631-252c-4e3c-820a-9e7ef4ef4da1)
 Call ID: 50150631-252c-4e3c-820a-9e7ef4ef4da1
  Args:
    type: :Woman
    source: :PrincessCecilia
  AssignClass (9ff8c376-148d-4e8f-9e65-b78feb962261)
 Call ID: 9ff8c376-148d-4e8f-9e65-b78feb962261
  Args:
    type: :Person
    source: :PrincessCecilia
  AddTriple (4dea69da-990d-45ab-94ea-f73f3bdfd1e1)
 Call ID: 4dea69da-990d-45ab-94ea-f73f3bdfd1e1
  Args:
    target: :PrinceCarlos
    source: :PrincessLuisa
    relation: :hasFather
  AddTriple (99168500-794f-437b-b79e-9f4d776c4089)
 Call ID: 99168500-794f-437b-b79e-9f4d776c4089
  Args:
    target: :PrinceCarlos
    source: :PrincessCecilia
    relation: :hasFather
  AssignClass (b7d08c88-3c63-4874-af38-c15302f75ace)
 Call ID: b7d08c88-3c63-4874-af38-c15302f75ace
  Args:
    type: :Woman
    source: :AnnemarieGualtherieVanWeezel
  AssignClass (d69daf4d-ef1e-45f5-8d2c-1a542089a6ae)
 Call ID: d69daf4d-ef1e-45f5-8d2c-1a542089a6ae
  Args:
    type: :Person
    source: :AnnemarieGualtherieVanWeezel
  AddTriple (49eb97dc-6ef5-43f9-9631-14b8047f5cca)
 Call ID: 49eb97dc-6ef5-43f9-9631-14b8047f5cca
  Args:
    source: :PrinceCarlosEnrique
    target: :AnnemarieGualtherieVanWeezel
    relation: :hasMother
  AddTriple (a16da46b-7ded-4cd5-8723-95c38cada15c)
 Call ID: a16da46b-7ded-4cd5-8723-95c38cada15c
  Args:
    source: :PrincessLuisa
    target: :AnnemarieGualtherieVanWeezel
    relation: :hasMother
  AddTriple (d174203a-cf16-46d0-9e52-14ace3f920a9)
 Call ID: d174203a-cf16-46d0-9e52-14ace3f920a9
  Args:
    source: :PrincessCecilia
    target: :AnnemarieGualtherieVanWeezel
    relation: :hasMother
  Finish (ac6d8e5d-550f-46a4-a94e-c450fc303199)
 Call ID: ac6d8e5d-550f-46a4-a94e-c450fc303199
  Args: